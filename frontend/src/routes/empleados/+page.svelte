<script lang="ts">
	import type { Trabajador } from "$lib/types";
	import TableEmpleados from "./TableEmpleados.svelte";
	import ModalEmpleado from "./ModalEmpleado.svelte";
	import ModalEliminarEmpleado from "./ModalEliminarEmpleado.svelte";

	let trabajadores: Trabajador[] = [
		{
			worker_id: 1,
			first_name: "Carlos",
			last_name: "Hernández",
			phone: "6621122334",
			position: "Mecánico",
			nickname: "Carlitos"
		},
		{
			worker_id: 2,
			first_name: "Pedro",
			last_name: "Lopez",
			phone: "6622233445",
			position: "Electricista"
		}
	];

	let mostrarModal = false;
	let mostrarModalEliminar = false;

	let trabajadorSeleccionado: Trabajador | null = null;
	let trabajadorAEliminar: Trabajador | null = null;

	// Crear
	function nuevoTrabajador() {
		trabajadorSeleccionado = null;
		mostrarModal = true;
	}

	// Editar
	function editarTrabajador(t: Trabajador) {
		trabajadorSeleccionado = t;
		mostrarModal = true;
	}

	// Guardar
	function guardarTrabajador(t: Trabajador) {
		if (trabajadorSeleccionado) {
			trabajadores = trabajadores.map(
				(tr) => (tr.worker_id === trabajadorSeleccionado!.worker_id ? t : tr)
			);
		} else {
			t.worker_id = Date.now(); // temporal
			trabajadores = [...trabajadores, t];
		}
		mostrarModal = false;
	}

	// Abrir modal eliminar
	function eliminarTrabajador(t: Trabajador) {
		trabajadorAEliminar = t;
		mostrarModalEliminar = true;
	}

	// Confirmar eliminación
	function confirmarEliminacion(t: Trabajador) {
		trabajadores = trabajadores.filter((tr) => tr.worker_id !== t.worker_id);
		mostrarModalEliminar = false;
	}
</script>

<div class="mt-4 flex justify-end mb-3">
	<button
		on:click={nuevoTrabajador}
		class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
	>
		Nuevo Trabajador
	</button>
</div>

<TableEmpleados
	{trabajadores}
	onEditar={editarTrabajador}
	onEliminar={eliminarTrabajador}
/>

{#if mostrarModal}
	<ModalEmpleado
		{trabajadorSeleccionado}
		onClose={() => (mostrarModal = false)}
		onGuardar={guardarTrabajador}
	/>
{/if}

{#if mostrarModalEliminar && trabajadorAEliminar}
	<ModalEliminarEmpleado
		trabajador={trabajadorAEliminar}
		onClose={() => (mostrarModalEliminar = false)}
		onConfirm={confirmarEliminacion}
	/>
{/if}
