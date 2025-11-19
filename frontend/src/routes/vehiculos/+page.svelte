<script lang="ts">
	import type { CarWithOwner } from "$lib/types";
	import TableVehiculos from "./TableVehiculos.svelte";

	// MOCK DATA temporal
	let vehiculos: CarWithOwner[] = [
		{
			car_id: 1,
			year: 2015,
			brand: "Honda",
			model: "Civic",
			license_plate: "WER-123",
			color: "Rojo",
			owner_name: "Carlos López",
			customer_id: 10
		},
		{
			car_id: 2,
			year: 2018,
			brand: "Toyota",
			model: "Corolla",
			license_plate: "XYZ-987",
			color: "Blanco",
			owner_name: "María Pérez",
			customer_id: 12
		}
	];
</script>

<h1 class="text-xl font-semibold text-gray-700 mb-4">Vehículos registrados</h1>

<TableVehiculos {vehiculos} />
