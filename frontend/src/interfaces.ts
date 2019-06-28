export interface IDataSource {
    id: string;
    name: string;
    api_uri?: string;
    web_uri?: string;
    coordinates: Array<number>;
}