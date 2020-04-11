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
 * @param perPage
 * @returns {Promise<any>}
 */
export const getQuestions = (page, perPage = 10) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${apiUrl}/questions?page=${page}&per_page=${perPage}`,
            type: 'GET',
            success: resolve,
            error: reject
        });
    });
};

/**
 * @description Search questions
 * @param searchTerm
 * @returns {Promise<any>}
 */
export const searchQuestions = (searchTerm = '') => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${apiUrl}/questions/searches`,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                search_term: searchTerm
            }),
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

/**
 * @description Delete question
 * @param id
 * @returns {Promise<any>}
 */
export const deleteQuestion = (id) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${apiUrl}/questions/${id}`,
            type: 'DELETE',
            success: resolve,
            error: reject
        });
    });
};

/**
 * @description Get category questions
 * @param categoryId
 * @returns {Promise<any>}
 */
export const getCategoryQuestions = (categoryId) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${apiUrl}/categories/${categoryId}/questions`,
            type: 'GET',
            success: resolve,
            error: reject
        });
    });
};

export const playQuiz = (category, previousQuestions = []) => {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: `${apiUrl}/quizzes`,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                previous_questions: previousQuestions,
                quiz_category: category
            }),
            success: resolve,
            error: reject
        });
    });
};