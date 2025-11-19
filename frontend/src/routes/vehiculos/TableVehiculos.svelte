<script lang="ts">
	import type { CarWithOwner } from "$lib/types";

	export let vehiculos: CarWithOwner[] = [];
</script>

<div class="bg-white shadow-sm border border-gray-200 rounded-lg p-6">
	<h2 class="text-lg font-semibold text-gray-700 mb-4">Lista de vehículos</h2>

	<div class="overflow-x-auto">
		<table class="w-full text-sm text-gray-700">
			<thead>
				<tr class="bg-gray-100 text-xs text-gray-600 uppercase">
					<th class="px-4 py-3 text-left">ID</th>
					<th class="px-4 py-3 text-left">Año</th>
					<th class="px-4 py-3 text-left">Marca</th>
					<th class="px-4 py-3 text-left">Modelo</th>
					<th class="px-4 py-3 text-left">Placas</th>
					<th class="px-4 py-3 text-left">Color</th>
					<th class="px-4 py-3 text-left">Cliente</th>
				</tr>
			</thead>

			<tbody>
				{#each vehiculos as v, i}
					<tr class={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
						<td class="px-4 py-3">{v.car_id}</td>
						<td class="px-4 py-3">{v.year}</td>
						<td class="px-4 py-3">{v.brand}</td>
						<td class="px-4 py-3">{v.model}</td>
						<td class="px-4 py-3">{v.license_plate}</td>
						<td class="px-4 py-3">{v.color}</td>
						<td class="px-4 py-3">{v.owner_name}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
	