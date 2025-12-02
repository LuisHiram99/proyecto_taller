// src/routes/logout/+server.ts
import type { RequestHandler } from './$types';
import { redirect } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ cookies }) => {
  cookies.delete('access_token', { path: '/' });
  throw redirect(303, '/login');
};
