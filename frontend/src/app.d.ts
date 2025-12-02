// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		 interface Locals {
			token: string | null;
			user: {
				user_id: number;
				email: string;
				first_name: string;
				last_name: string;
				role: 'admin' | 'manager' | 'worker';
				workshop_id: number;
			} | null;
		 }
		 interface PageData {
			user: Locals['user'];
			isLoggedIn: boolean;
			// Podemos pasar mensajes extra (como razón de redirecciones)
			message?: string | null;
		 }
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
