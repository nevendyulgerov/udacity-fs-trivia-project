import React, {Component} from 'react';
import { getCategories, createQuestion } from '../api';
import '../stylesheets/FormView.css';

class FormView extends Component {
    constructor() {
        super();
        this.state = {
            question: '',
            answer: '',
            difficulty: 1,
            category: 1,
            categories: {}
        }
    }

    componentDidMount() {
        getCategories()
            .then((result) => {
                this.setState({
                    categories: result.categories
                });
            })
            .catch(() => {
                alert('Unable to load categories. Please try your request again');
            });
    }


    submitQuestion = (event) => {
        event.preventDefault();
        const { question, answer, difficulty, category } = this.state;
        const questionBody = {
            question,
            answer,
            difficulty,
            category
        };

        createQuestion(questionBody)
            .then(() => {
                document.getElementById("add-question-form").reset();
            })
            .catch(() => {
                alert('Unable to add question. Please try your request again');
            });
    };

    handleChange = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        })
    };

    render() {
        return (
            <div id="add-form">
                <h2>Add a New Trivia Question</h2>
                <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
                    <label>
                        Question
                        <input type="text" name="question" onChange={this.handleChange}/>
                    </label>
                    <label>
                        Answer
                        <input type="text" name="answer" onChange={this.handleChange}/>
                    </label>
                    <label>
                        Difficulty
                        <select name="difficulty" onChange={this.handleChange}>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </label>
                    <label>
                        Category
                        <select name="category" onChange={this.handleChange}>
                            {Object.keys(this.state.categories).map(id => {
                                return (
                                    <option key={id} value={id}>{this.state.categories[id]}</option>
                                )
                            })}
                        </select>
                    </label>
                    <input type="submit" className="button" value="Submit"/>
                </form>
            </div>
        );
    }
}

export default FormView;
