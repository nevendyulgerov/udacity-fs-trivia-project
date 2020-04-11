import React, {Component} from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import { getQuestions, getCategoryQuestions, searchQuestions, deleteQuestion } from '../api';

class QuestionView extends Component {
    constructor() {
        super();
        this.perPage = 10;
        this.state = {
            questions: [],
            page: 1,
            totalQuestions: 0,
            categories: {},
            currentCategory: null,
        };
    }

    componentDidMount() {
        this.getQuestions();
    }

    getQuestions = () => {
        const { page } = this.state;

        getQuestions(page, this.perPage)
            .then((result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    categories: result.categories,
                    currentCategory: result.current_category
                })
            })
            .catch(() => {
                alert('Unable to load questions. Please try your request again');
            });
    };

    selectPage(num) {
        this.setState({page: num}, () => this.getQuestions());
    }

    createPagination() {
        let pageNumbers = [];
        let maxPage = Math.ceil(this.state.totalQuestions / this.perPage);

        for (let i = 1; i <= maxPage; i++) {
            pageNumbers.push(
                <span
                    key={i}
                    className={`page-num ${i === this.state.page ? 'active' : ''}`}
                    onClick={() => this.selectPage(i)}
                >
                    {i}
                </span>
            )
        }
        return pageNumbers;
    }

    getByCategory = (id) => {
        getCategoryQuestions(id)
            .then((result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category
                })
            })
            .catch(() => {
                alert('Unable to load questions. Please try your request again')
            });
    };

    submitSearch = (searchTerm) => {
        searchQuestions(searchTerm)
            .then((result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category
                })
            })
            .catch(() => {
                alert('Unable to load questions. Please try your request again')
            });
    };

    questionAction = (id) => (action) => {
        if (action === 'DELETE' && window.confirm('are you sure you want to delete the question?')) {
            deleteQuestion(id)
                .then(() => this.onDeleteQuestion(id))
                .catch(() => {
                    alert('Unable to load questions. Please try your request again')
                });
        }
    };

    onDeleteQuestion = (id) => {
        const { page, questions } = this.state;
        const remainingQuestions = questions.filter((question) => question.id !== id);
        // use the same page if there are some remaining questions or this is the first page, otherwise use the previous page
        const nextPage = remainingQuestions.length > 0 || page - 1 < 0
            ? page
            : page - 1;

        this.setState({
            page: nextPage
        }, () => this.getQuestions())
    };

    render() {
        return (
            <div className="question-view">
                <div className="categories-list">
                    <h2 onClick={this.getQuestions}>
                        Categories
                    </h2>

                    <ul>
                        {Object.keys(this.state.categories).map((id,) => (
                            <li
                                key={id}
                                onClick={() => this.getByCategory(id)}
                            >
                                {this.state.categories[id]}

                                <img
                                    className="category"
                                    src={`${this.state.categories[id]}.svg`}
                                />
                            </li>
                        ))}
                    </ul>

                    <Search submitSearch={this.submitSearch}/>
                </div>

                <div className="questions-list">
                    <h2>Questions</h2>

                    {this.state.questions.map((q) => (
                        <Question
                            key={q.id}
                            question={q.question}
                            answer={q.answer}
                            category={this.state.categories[q.category]}
                            difficulty={q.difficulty}
                            questionAction={this.questionAction(q.id)}
                        />
                    ))}

                    <div className="pagination-menu">
                        {this.createPagination()}
                    </div>
                </div>
            </div>
        );
    }
}

export default QuestionView;
