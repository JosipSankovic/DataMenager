import type { ProjectBase } from "../api";
import { createContext, type Dispatch, type SetStateAction } from "react";


export interface ProjectContextType{
    project:ProjectBase|null,
    setProject:Dispatch<SetStateAction<ProjectBase|null>>
}
export const ProjectContext = createContext<ProjectContextType|null>(null)