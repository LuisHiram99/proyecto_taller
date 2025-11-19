<script lang="ts">
	import type { Cliente } from "$lib/types";

	export let clientes: Cliente[] = [];
	export let onEditar: (c: Cliente) => void;
	export let onEliminar: (c: Cliente) => void;
</script>

<div class="bg-white shadow-sm border border-gray-200 rounded-lg p-6">
	<h2 class="text-lg font-semibold text-gray-700 mb-4">
		Lista de clientes
	</h2>

	<div class="overflow-x-auto">
		<table class="w-full text-sm text-gray-700 border-collapse">
			<thead>
				<tr class="bg-gray-100 text-gray-600 uppercase text-xs">
					<th class="px-4 py-3 text-left">ID</th>
					<th class="px-4 py-3 text-left">Nombre</th>
					<th class="px-4 py-3 text-left">Teléfono</th>
					<th class="px-4 py-3 text-left">Correo</th>
					<th class="px-4 py-3 text-center">Acción</th>
				</tr>
			</thead>

			<tbody>
				{#each clientes as c, i}
					<tr class={i % 2 === 0 ? "bg-white" : "bg-gray-200"}>
						<td class="px-4 py-3">{c.customer_id}</td>
						<td class="px-4 py-3">{c.first_name} {c.last_name}</td>
						<td class="px-4 py-3">{c.phone}</td>
						<td class="px-4 py-3">{c.email ?? "—"}</td>

						<td class="px-4 py-3 text-center flex">
							<button
								on:click={() => onEditar(c)}
								class="w-7 h-7 rounded bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition"
							>
								<svg class="w-4 h-4 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
									<path
										d="M17.414 2.586a2 2 0 00-2.828 0l-9.9 9.9a1 1 0 00-.263.47l-1 4a1 1 0 001.213 1.213l4-1a1 1 0 00.47-.263l9.9-9.9a2 2 0 000-2.828l-1.592-1.592zM5.121 13.879l-.586 2.344 2.344-.586 9.193-9.193-1.758-1.758L5.12 13.88z"
									/>
								</svg>
								
							</button>
							<!-- ELIMINAR -->
							<button
								on:click={() => onEliminar(c)}
								class="w-7 h-7 rounded bg-red-200 hover:bg-red-300 flex items-center justify-center"
							>
								<svg class="w-4 h-4 text-red-700" fill="currentColor" viewBox="0 0 20 20">
									<path
										fill-rule="evenodd"
										d="M9 2a1 1 0 00-.894.553L7.382 4H3a1 1 0 000 2h1v10a2 2 0 002 2h8a2 2 0 002-2V6h1a1 1 0 100-2h-4.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
										clip-rule="evenodd"
									/>
								</svg> 
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
