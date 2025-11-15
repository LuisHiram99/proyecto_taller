<script lang="ts">
	import TableVehiculos from './TableVehiculos.svelte';

	// MOCK DATA DE VEHÍCULOS
	const vehiculos = [
		{
			customer_car_id: 1,
			license_plate: "VZA-334",
			color: "Gris",
			customer: { first_name: "Juan", last_name: "Pérez" },
			car: { brand: "Nissan", model: "Versa", year: 2019 }
		},
		{
			customer_car_id: 2,
			license_plate: "YTR-921",
			color: "Rojo",
			customer: { first_name: "María", last_name: "López" },
			car: { brand: "Mazda", model: "3", year: 2020 }
		},
		{
			customer_car_id: 3,
			license_plate: "XSD-553",
			color: "Blanco",
			customer: { first_name: "Pedro", last_name: "Ramírez" },
			car: { brand: "Toyota", model: "Corolla", year: 2018 }
		}
	];
</script>

<div class="mt-4">
	<TableVehiculos {vehiculos} />
</div>
