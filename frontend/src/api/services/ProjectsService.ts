/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ProjectBase } from '../models/ProjectBase';
import type { ProjectCreate } from '../models/ProjectCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ProjectsService {
    /**
     * Create Project
     * @param requestBody
     * @returns ProjectBase Successful Response
     * @throws ApiError
     */
    public static createProjectProjectsPost(
        requestBody: ProjectCreate,
    ): CancelablePromise<ProjectBase> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/projects/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Read Projects
     * @param skip
     * @param limit
     * @returns ProjectBase Successful Response
     * @throws ApiError
     */
    public static readProjectsProjectsGet(
        skip?: number,
        limit: number = 100,
    ): CancelablePromise<Array<ProjectBase>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/projects/',
            query: {
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Project
     * @param projectId
     * @returns ProjectBase Successful Response
     * @throws ApiError
     */
    public static getProjectProjectsProjectIdGet(
        projectId: string,
    ): CancelablePromise<ProjectBase> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/projects/{project_id}',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Project
     * @param projectId
     * @returns ProjectBase Successful Response
     * @throws ApiError
     */
    public static deleteProjectProjectsProjectIdDelete(
        projectId: string,
    ): CancelablePromise<ProjectBase> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/projects/{project_id}',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
