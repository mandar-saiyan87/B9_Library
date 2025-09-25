import React, { Suspense } from "react"
import Navbar from "./components/Navbar"
import { Outlet } from "react-router"

function App() {


  return (
    <>
      <Navbar />
      <div className="w-full max-w-[1536px] flex-center flex-col mx-auto">
        <Suspense fallback={<div>Loading...</div>}>
          <Outlet />
        </Suspense>
      </div>
    </>
  )
}

export default App
