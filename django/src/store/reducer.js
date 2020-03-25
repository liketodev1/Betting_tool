import { createStore, compose } from 'redux';
import createReducer from './createReducer';
import {SET_POSTS, RESET_STATE} from './actions';

const defaultState = {
    posts: null
};

const reducer = createReducer(defaultState, {
    [SET_POSTS]: (state, action) => ({
        ...state,   
        posts: action.posts,
    }),
    [RESET_STATE]: () => defaultState,
});

const store = createStore(reducer, compose);

export default store;