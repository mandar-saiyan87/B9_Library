import { createBrowserRouter } from "react-router";
import App from "../App";
import Homepage from "../pages/Homepage";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            {
                index: true,
                element: <Homepage />
            }
        ]
    },
]);

export default router