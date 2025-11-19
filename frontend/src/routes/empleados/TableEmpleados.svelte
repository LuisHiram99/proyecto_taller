<script lang="ts">
	import type { Trabajador } from "$lib/types";

	export let trabajadores: Trabajador[] = [];
	export let onEditar: (t: Trabajador) => void;
	export let onEliminar: (t: Trabajador) => void;
</script>

<div class="bg-white shadow-sm border border-gray-200 rounded-lg p-6">
	<h2 class="text-lg font-semibold text-gray-700 mb-4">Lista de trabajadores</h2>

	<div class="overflow-x-auto">
		<table class="w-full text-sm text-gray-700">
			<thead>
				<tr class="bg-gray-100 text-xs text-gray-600 uppercase">
					<th class="px-4 py-3 text-left">ID</th>
					<th class="px-4 py-3 text-left">Nombre</th>
					<th class="px-4 py-3 text-left">Teléfono</th>
					<th class="px-4 py-3 text-left">Puesto</th>
					<th class="px-4 py-3 text-center">Acción</th>
				</tr>
			</thead>

			<tbody>
				{#each trabajadores as t, i}
					<tr class={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
						<td class="px-4 py-3">{t.worker_id}</td>
						<td class="px-4 py-3">{t.first_name} {t.last_name}</td>
						<td class="px-4 py-3">{t.phone ?? "—"}</td>
						<td class="px-4 py-3">{t.position}</td>

						<td class="px-4 py-3 flex gap-2 justify-center">

							<!-- EDITAR -->
							<button
								on:click={() => onEditar(t)}
								class="w-7 h-7 bg-gray-200 hover:bg-gray-300 rounded flex items-center justify-center"
							>
								<svg class="w-4 h-4 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
									<path
										d="M17.414 2.586a2 2 0 00-2.828 0l-9.9 9.9a1 1 0 00-.263.47l-1 4a1 1 0 001.213 1.213l4-1a1 1 0 00.47-.263l9.9-9.9a2 2 0 000-2.828z"
									/>
								</svg>
							</button>

							<!-- ELIMINAR -->
							<button
								on:click={() => onEliminar(t)}
								class="w-7 h-7 bg-red-200 hover:bg-red-300 rounded flex items-center justify-center"
							>
								<svg class="w-4 h-4 text-red-700" fill="currentColor" viewBox="0 0 20 20">
									<path
										fill-rule="evenodd"
										d="M9 2a1 1 0 00-.894.553L7.382 4H3a1 1 0 000 2h1v10a2 2 0 002 2h8a2 2 0 002-2V6h1a1 1 0 000-2h-4.382l-.724-1.447z"
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
