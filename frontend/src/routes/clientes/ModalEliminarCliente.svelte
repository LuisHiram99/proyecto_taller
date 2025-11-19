<script lang="ts">
	import type { Cliente } from "$lib/types";

	export let cliente: Cliente;
	export let onClose: () => void;
	export let onConfirm: (c: Cliente) => void;
</script>

<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
	<div class="bg-white w-full max-w-sm rounded-lg shadow-lg p-6 animate-fadeIn">

		<h2 class="text-lg font-semibold text-gray-700 mb-3">
			Eliminar Cliente
		</h2>

		<p class="text-gray-600 text-sm mb-4">
			¿Estás seguro de que deseas eliminar al cliente
			<strong>{cliente.first_name} {cliente.last_name}</strong>?
		</p>

		<div class="flex justify-end gap-2">
			<button
				on:click={onClose}
				class="px-4 py-2 bg-gray-300 hover:bg-gray-400 rounded-lg"
			>
				Cancelar
			</button>

			<button
				on:click={() => onConfirm(cliente)}
				class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg"
			>
				Eliminar
			</button>
		</div>

	</div>
</div>

<style>
	@keyframes fadeIn {
		from { opacity: 0; transform: scale(0.95); }
		to { opacity: 1; transform: scale(1); }
	}

	.animate-fadeIn {
		animation: fadeIn 0.2s ease-out forwards;
	}
</style>
