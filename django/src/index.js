import React, { lazy, Suspense } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
// import App from './App';
import { Provider } from 'react-redux'
import store from "../src/store/reducer"
import * as serviceWorker from './serviceWorker';

const App = lazy(() => import('./App'))

ReactDOM.render(<Provider store={store}>
    <Suspense fallback={<h1>Still Loading…</h1>}>
        <App />
    </Suspense>
</Provider>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

