import $ from 'jquery';

export const apiUrl = 'http://localhost:8000/api/v1';

/**
 * @desc Get categories
 * @returns {Promise<any>}
 */
export const getCategories = () => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${apiUrl}/categories`,
            type: 'GET',
            success: resolve,
            error: reject
        });
    });
};

/**
 * @description Get questions
 * @param page
 * @returns {Promise<any>}
 */
export const getQuestions = (page) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${apiUrl}/questions?page=${page}`,
            type: 'GET',
            success: resolve,
            error: reject
        });
    });
};

/**
 * @description Create question
 * @param question
 * @returns {Promise<any>}
 */
export const createQuestion = (question) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${apiUrl}/questions`,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(question),
            success: resolve,
            error: reject
        })
    });
};