import { getCalculationTypes } from "../api";
import { useCalculationStore } from "../stores/calculationStore";



export class Calculator {
    constructor() {
        this.store = useCalculationStore();
    }

    async loadModelTypes() {
        
        this.store.setLoading(true);
        const response = await getCalculationTypes();
        const types = response.data;
        console.log("Loaded calculation types:", response.data);

        this.store.setLoading(false);
        return types;

    }

}