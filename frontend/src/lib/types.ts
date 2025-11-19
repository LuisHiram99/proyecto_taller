export interface Cliente {
    customer_id?: number; // opcional al crear
    first_name: string;
    last_name: string;
    phone: string;
    email?: string;
    workshop_id?: number;
}

export interface Trabajador {
    worker_id?: number;
    first_name: string;
    last_name: string;
    phone?: string;
    position: string;
    nickname?: string;
    workshop_id?: number;
}

export interface Car {
    car_id?: number;
    year: number;
    brand: string;
    model: string;
}

export interface CustomerCar {
    customer_car_id?: number;
    customer_id: number;
    car_id: number;
    license_plate: string;
    color?: string;
}

export interface CarWithOwner extends Car {
    license_plate: string;
    color?: string;
    owner_name: string;
    customer_id: number;
}
