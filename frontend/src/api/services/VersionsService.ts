/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { VersionBase } from '../models/VersionBase';
import type { VersionCreate } from '../models/VersionCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class VersionsService {
    /**
     * Get Versions
     * @param projectId
     * @param offset
     * @param limit
     * @returns VersionBase Successful Response
     * @throws ApiError
     */
    public static getVersionsVersionsGet(
        projectId?: any,
        offset?: number,
        limit: number = 100,
    ): CancelablePromise<Array<VersionBase>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/versions/',
            query: {
                'project_id': projectId,
                'offset': offset,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Version
     * @param requestBody
     * @returns VersionBase Successful Response
     * @throws ApiError
     */
    public static addVersionVersionsPost(
        requestBody: VersionCreate,
    ): CancelablePromise<VersionBase> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/versions/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
