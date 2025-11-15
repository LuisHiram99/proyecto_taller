<script lang="ts">
	import '../app.css';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import Hero from '$lib/components/Hero.svelte';
</script>

<div class="flex h-screen bg-white text-gray-800">
	<Sidebar />

	<div class="flex-1 ml-49 flex flex-col"> <!-- ml debe coincidir con el width del sidebar -->
		<Hero empresa="Los Chinos" />

		<main class="flex-1 p-6 overflow-y-auto bg-gray-50">
			<slot />
		</main>
	</div>
</div>
