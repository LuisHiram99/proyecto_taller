<script lang="ts">
	export let empleados = [];
</script>

<div class="bg-white shadow-sm border border-gray-200 rounded-lg p-6">
	<h2 class="text-lg font-semibold text-gray-700 mb-4">
		Lista de trabajadores
	</h2>

	<div class="overflow-x-auto">
		<table class="w-full text-sm text-gray-700 border-collapse">
			<thead>
				<tr class="bg-gray-100 text-gray-600 uppercase text-xs">
					<th class="px-4 py-3 text-left">ID</th>
					<th class="px-4 py-3 text-left">Nombre</th>
					<th class="px-4 py-3 text-left">Apodo</th>
					<th class="px-4 py-3 text-left">Teléfono</th>
					<th class="px-4 py-3 text-left">Puesto</th>
					<th class="px-4 py-3 text-left">Sucursal</th>
					<th class="px-4 py-3 text-center">Acción</th>
				</tr>
			</thead>

			<tbody>
				{#each empleados as w, i}
					<tr class={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
						<td class="px-4 py-3">{w.worker_id}</td>
						<td class="px-4 py-3">{w.first_name} {w.last_name}</td>
						<td class="px-4 py-3">{w.nickname || "—"}</td>
						<td class="px-4 py-3">{w.phone || "—"}</td>
						<td class="px-4 py-3">{w.position}</td>
						<td class="px-4 py-3">{w.workshop_id}</td>

						<td class="px-4 py-3 text-center">
							<button
								class="w-7 h-7 rounded bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition"
								title="Editar"
							>
								<svg class="w-4 h-4 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
									<path
										d="M17.414 2.586a2 2 0 00-2.828 0l-9.9 9.9a1 1 0 00-.263.47l-1 4a1 1 0 001.213 1.213l4-1a1 1 0 00.47-.263l9.9-9.9a2 2 0 000-2.828l-1.592-1.592zM5.121 13.879l-.586 2.344 2.344-.586 9.193-9.193-1.758-1.758L5.12 13.88z"
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
