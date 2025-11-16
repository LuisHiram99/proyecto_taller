<script lang="ts">
	import TablePiezas from './TablePiezas.svelte';

	// MOCK DATA (temporal)
	const piezas = [
		{
			part_id: 1,
			part_name: "Filtro de Aceite",
			brand: "FRAM",
			category: "Filtros",
			description: "Filtro de aceite para motor 1.6 L"
		},
		{
			part_id: 2,
			part_name: "Bujía de Encendido",
			brand: "NGK",
			category: "Ignición",
			description: "Bujía estándar para motores de 4 cilindros"
		},
		{
			part_id: 3,
			part_name: "Pastillas de Freno",
			brand: "Brembo",
			category: "Frenos",
			description: "Juego de pastillas delanteras"
		}
	];
</script>

<div class="mt-4">
	<TablePiezas {piezas} />
</div>
