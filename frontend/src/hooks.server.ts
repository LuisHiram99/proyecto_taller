// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const handle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('access_token') ?? null;

  event.locals.token = token;
  event.locals.user = null;

  if (token) {
    try {
      const res = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/me/`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: 'application/json'
        }
      });

      if (res.ok) {
        const user = await res.json();

        event.locals.user = {
          user_id: user.user_id,
          email: user.email,
          first_name: user.first_name,
          last_name: user.last_name,
          role: user.role,
          workshop_id: user.workshop_id
        };
      } else if (res.status === 401) {
        // Token inválido/expirado: limpiamos cookie
        event.cookies.delete('access_token', { path: '/' });
        event.locals.token = null;
      }
    } catch (error) {
      console.error('Error obteniendo /me:', error);
      // Si el backend está caído, no rompemos la app, pero no habrá usuario
    }
  }

  const response = await resolve(event);
  return response;
};
