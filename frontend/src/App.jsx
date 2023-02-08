import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import StoreProvider, { StoreContext } from './Utils/store';
import PageRoutes from './Pages/PageRoutes';

function App() {
	const context = React.useContext(StoreContext);
	return (
			<BrowserRouter>
				<StoreProvider>
					<PageRoutes></PageRoutes>
				</StoreProvider>
			</BrowserRouter>
	);
}

export default App;
