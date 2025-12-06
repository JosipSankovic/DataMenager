/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DatasetAll } from '../models/DatasetAll';
import type { DatasetBase } from '../models/DatasetBase';
import type { DatasetCreate } from '../models/DatasetCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DatasetService {
    /**
     * Get All
     * @param projectId
     * @returns DatasetBase Successful Response
     * @throws ApiError
     */
    public static getAllDatasetAllGet(
        projectId: string,
    ): CancelablePromise<Array<DatasetBase>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/dataset/all',
            query: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All
     * @param requestBody
     * @returns DatasetAll Successful Response
     * @throws ApiError
     */
    public static getAllDatasetAllverPost(
        requestBody: DatasetCreate,
    ): CancelablePromise<DatasetAll> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/dataset/allver',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get
     * @param datasetId
     * @param projectId
     * @returns DatasetBase Successful Response
     * @throws ApiError
     */
    public static getDatasetGet(
        datasetId: string,
        projectId: string,
    ): CancelablePromise<Array<DatasetBase>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/dataset/',
            query: {
                'dataset_id': datasetId,
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Dataset
     * @param requestBody
     * @returns DatasetBase Successful Response
     * @throws ApiError
     */
    public static createDatasetDatasetPost(
        requestBody: DatasetCreate,
    ): CancelablePromise<DatasetBase> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/dataset/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
