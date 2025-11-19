<script lang="ts">
	import type { Cliente } from "$lib/types";

	export let clienteSeleccionado: Cliente | null = null;
	export let onClose: () => void;
	export let onGuardar: (c: Cliente) => void;

	let form: Cliente = clienteSeleccionado
		? { ...clienteSeleccionado }
		: { first_name: "", last_name: "", phone: "", email: "" };
</script>

<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
	<div class="bg-white w-full max-w-md rounded-lg shadow-lg p-6 animate-fadeIn">

		<h2 class="text-xl font-semibold text-gray-700 mb-4">
			{clienteSeleccionado ? "Editar Cliente" : "Nuevo Cliente"}
		</h2>

		<div class="space-y-3">
			<input
				class="w-full border border-gray-300 rounded px-3 py-2"
				placeholder="Nombre"
				bind:value={form.first_name}
			/>

			<input
				class="w-full border border-gray-300 rounded px-3 py-2"
				placeholder="Apellido"
				bind:value={form.last_name}
			/>

			<input
				class="w-full border border-gray-300 rounded px-3 py-2"
				placeholder="Teléfono"
				bind:value={form.phone}
			/>

			<input
				class="w-full border border-gray-300 rounded px-3 py-2"
				placeholder="Correo (opcional)"
				bind:value={form.email}
			/>
		</div>

		<div class="flex justify-end gap-2 mt-5">
			<button on:click={onClose} class="px-4 py-2 bg-gray-300 hover:bg-gray-400 rounded-lg">
				Cancelar
			</button>

			<button
				on:click={() => onGuardar(form)}
				class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
			>
				Guardar
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
