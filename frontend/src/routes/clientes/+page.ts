import { pageMetadata } from '$lib/state/pageMetadata';

export const load = () => {
	pageMetadata.set({ title: 'Clientes' });
};
