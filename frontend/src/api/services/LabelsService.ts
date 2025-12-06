/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { LabelBase } from '../models/LabelBase';
import type { LabelCreate } from '../models/LabelCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LabelsService {
    /**
     * Get Labels
     * @param versionId
     * @param projectId
     * @param useNonVersioned
     * @param offset
     * @param limit
     * @returns LabelBase Successful Response
     * @throws ApiError
     */
    public static getLabelsLabelsGet(
        versionId: string,
        projectId: string,
        useNonVersioned: boolean = true,
        offset?: number,
        limit: number = 10000,
    ): CancelablePromise<Array<LabelBase>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/labels/',
            query: {
                'version_id': versionId,
                'project_id': projectId,
                'use_non_versioned': useNonVersioned,
                'offset': offset,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Label
     * @param requestBody
     * @returns LabelBase Successful Response
     * @throws ApiError
     */
    public static addLabelLabelsPost(
        requestBody: LabelCreate,
    ): CancelablePromise<LabelBase> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/labels/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Image Label
     * @param imageId
     * @param versionId
     * @returns LabelBase Successful Response
     * @throws ApiError
     */
    public static getImageLabelLabelsGetImageLabelGet(
        imageId: string,
        versionId?: string,
    ): CancelablePromise<LabelBase> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/labels/get-image-label',
            query: {
                'image_id': imageId,
                'version_id': versionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
