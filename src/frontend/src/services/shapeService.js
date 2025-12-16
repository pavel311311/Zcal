/**
 * 形状数据服务 - 加载和处理形状数据
 */

export class ShapeService {
    /**
     * 加载形状数据
     * @returns {Promise} 形状数据Promise
     */
    async loadShapeData() {
        try {
            const response = await fetch('/shapes.json');
            if (!response.ok) {
                throw new Error('Failed to load shape data');
            }
            const data = await response.json();
            return data.lines;
        } catch (error) {
            console.error('Error loading shape data:', error);
            return [];
        }
    }
}
