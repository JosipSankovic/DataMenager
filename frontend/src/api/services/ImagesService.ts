/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ImageBase } from '../models/ImageBase';
import type { ImageCreate } from '../models/ImageCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ImagesService {
    /**
     * Get All
     * @param projectId
     * @param skip
     * @param limit
     * @returns ImageBase Successful Response
     * @throws ApiError
     */
    public static getAllImagesGet(
        projectId: string,
        skip?: number,
        limit: number = 100,
    ): CancelablePromise<Array<ImageBase>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/images/',
            query: {
                'project_id': projectId,
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Image
     * @param requestBody
     * @returns ImageBase Successful Response
     * @throws ApiError
     */
    public static createImageImagesPost(
        requestBody: ImageCreate,
    ): CancelablePromise<ImageBase> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/images/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Img To Project
     * @param imgsDir
     * @param projectId
     * @param requestBody
     * @returns ImageBase Successful Response
     * @throws ApiError
     */
    public static addImgToProjectImagesAddImgsToProjectPost(
        imgsDir: string,
        projectId: string,
        requestBody: Array<string>,
    ): CancelablePromise<Array<ImageBase>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/images/add_imgs_to_project',
            query: {
                'imgs_dir': imgsDir,
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Folder Images
     * @param folderPath
     * @param page
     * @returns string Successful Response
     * @throws ApiError
     */
    public static getFolderImagesImagesFolderImagesGet(
        folderPath: string,
        page: number,
    ): CancelablePromise<Array<string>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/images/folder_images',
            query: {
                'folder_path': folderPath,
                'page': page,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Serve File
     * @param filePath
     * @returns any Successful Response
     * @throws ApiError
     */
    public static serveFileImagesServeImageGet(
        filePath: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/images/serve_image',
            query: {
                'file_path': filePath,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
