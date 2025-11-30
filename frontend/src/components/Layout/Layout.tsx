import { useContext, useEffect, useState, type ChangeEvent } from "react";
import { Link, Outlet } from "react-router";
import { ProjectsService, type ProjectBase } from "../../api";
import { ProjectContext } from "../../utils";
import "./Layout.css";

export default function Layout() {
  const [projects, setProjects] = useState<Array<ProjectBase>>([]);
  const [error, setError] = useState<string | null>(null);
  const projectContext = useContext(ProjectContext);
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const pr_resp = await ProjectsService.readProjectsProjectsGet(0, 100);
        setProjects(pr_resp);
      } catch (error) {
        console.error(error);
        setError("Error happend");
      }
    };
    fetchProjects();
  }, []);

  const optionChanged = (event: ChangeEvent<HTMLSelectElement>) => {
    const pr_id = event.target.value;
    const selected_pr_index = projects.findIndex((pr) => pr.id == pr_id);
    if (selected_pr_index < 0) {
      projectContext?.setProject(null);
    }
    projectContext?.setProject(projects[selected_pr_index]);
  };
  return (
    <>
      <div className="navigation-wrapper">
        <select onChange={(e) => optionChanged(e)}>
          <option>Select project</option>
          {projects.map((pr) => (
            <option key={pr.id} value={pr.id}>
              {pr.name}
            </option>
          ))}
        </select>
        {projectContext?.project?
        <nav>
          <Link to={"/"}>
            <span className="material-symbols-outlined">dashboard</span>
            Dashboard
          </Link>
          <Link to={"/datasets"}>
            <span
              className="material-symbols-outlined"
              style={{fontVariationSettings :"'FILL' 1"}}
            >
              database
            </span>
            Datasets
          </Link>
          <Link to={"/models"}>
            <span className="material-symbols-outlined">memory</span>Models
          </Link>
           <Link to={"/addimages"}>
            <span className="material-symbols-outlined">add</span>Add images
          </Link>
        </nav>:null}
      </div>
      <main className="main-wrapper">
      <Outlet />
      </main>
    </>
  );
}
