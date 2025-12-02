// @ts-nocheck
// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load = async ({ locals, url }: Parameters<LayoutServerLoad>[0]) => {
  // Rutas públicas (solo login y, si la usas, signup)
  const publicPaths = ['/login', '/signup'];
  const isPublic = publicPaths.includes(url.pathname);

  const user = locals.user;

  // 1) Si NO hay usuario y la ruta NO es pública → mandar a /login
  if (!user && !isPublic) {
    throw redirect(303, '/login');
  }

  // 2) Si HAY usuario y está intentando entrar a /login → mandarlo al inicio (/)
  if (user && url.pathname === '/login') {
    throw redirect(303, '/');
  }

  // 3) Si el usuario es worker → no debe usar el sistema
  if (user && user.role === 'worker') {
    // opcionalmente podrías hacer logout automático aquí si quieres
    throw redirect(303, '/login?reason=unauthorized');
  }

  // 4) Si intenta entrar a /admin y no es admin → mandarlo al inicio
  if (user && url.pathname.startsWith('/admin') && user.role !== 'admin') {
    throw redirect(303, '/');
  }

  // 5) (YA NO redirigimos / → /dashboard, porque tu dashboard ES /)

  return {
    user,
    isLoggedIn: !!user
  };
};
