<script lang="ts">
  import type { Cliente } from "$lib/types";
  import TableClientes from "./TableClientes.svelte";
  import ModalCliente from "./ModalCliente.svelte";
  import ModalEliminarCliente from "./ModalEliminarCliente.svelte";

  // TEMPORAL: datos de prueba (luego vendrán del backend)
  let clientes: Cliente[] = [
    {
      customer_id: 1,
      first_name: "Juanito",
      last_name: "Ramírez",
      phone: "6621234567",
      email: "juan@example.com",
    },
    {
      customer_id: 2,
      first_name: "María",
      last_name: "López",
      phone: "6629988776",
      email: "maria@example.com",
    },
  ];

  let mostrarModal = false;
  let mostrarModalEliminar = false;

  let clienteSeleccionado: Cliente | null = null;
  let clienteAEliminar: Cliente | null = null;

  // Crear
  function nuevoCliente() {
    clienteSeleccionado = null;
    mostrarModal = true;
  }

  // Editar
  function editarCliente(c: Cliente) {
    clienteSeleccionado = c;
    mostrarModal = true;
  }

  // Guardar (crear o editar)
  function guardarCliente(c: Cliente) {
    if (clienteSeleccionado) {
      // Editar existente
      clientes = clientes.map((cli) =>
        cli.customer_id === clienteSeleccionado!.customer_id ? c : cli
      );
    } else {
      // Crear nuevo
      c.customer_id = Date.now(); // temporal
      clientes = [...clientes, c];
    }

    mostrarModal = false;
  }

  // Eliminar
  function eliminarCliente(c: Cliente) {
    clienteAEliminar = c;
    mostrarModalEliminar = true;
  }

  function confirmarEliminacion(c: Cliente) {
    clientes = clientes.filter((cli) => cli.customer_id !== c.customer_id);
    mostrarModalEliminar = false;
  }
</script>

<!-- BOTÓN CREAR -->
<div class="mt-4 flex justify-end mb-3">
  <button
    on:click={nuevoCliente}
    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
  >
    Nuevo Cliente
  </button>
</div>

<!-- TABLA -->
<TableClientes {clientes} onEditar={editarCliente} onEliminar={eliminarCliente} />

<!-- MODAL CREAR / EDITAR -->
{#if mostrarModal}
  <ModalCliente
    {clienteSeleccionado}
    onClose={() => (mostrarModal = false)}
    onGuardar={guardarCliente}
  />
{/if}

<!-- MODAL ELIMINAR -->
{#if mostrarModalEliminar && clienteAEliminar}
  <ModalEliminarCliente
    cliente={clienteAEliminar}
    onClose={() => (mostrarModalEliminar = false)}
    onConfirm={confirmarEliminacion}
  />
{/if}
