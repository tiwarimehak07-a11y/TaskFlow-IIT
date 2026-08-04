const API_URL = "http://127.0.0.1:8000";

let tasks = [];


document.addEventListener("DOMContentLoaded", () => {

    loadCachedTasks();
    fetchTasks();
    loadProjects();

});

async function loadProjects(){

    try{

        const response = await fetch(`${API_URL}/projects`);

        const projects = await response.json();


        const projectSelect =
        document.getElementById("project");


        projects.forEach(project => {


            const option =
            document.createElement("option");


            option.value = project.id;


            option.textContent =
            project.name;


            projectSelect.appendChild(option);


        });


    }
    catch(error){

        console.log("Project loading error:", error);

    }

}



// LocalStorage se tasks load karna

function loadCachedTasks() {

    const cachedTasks = localStorage.getItem("tasks");

    if (cachedTasks) {

        tasks = JSON.parse(cachedTasks);

        renderTasks(tasks);

    }

}

// Error message

document.getElementById("title").addEventListener("input", function () {

    const error = document.getElementById("titleError");

    if (this.value.trim() !== "") {

        error.textContent = "";

    }

});


// Backend se tasks lana

async function fetchTasks() {

}
    try {

        const response = await fetch(`${API_URL}/tasks`);

        const data = await response.json();


        tasks = data;


        localStorage.setItem(
            "tasks",
            JSON.stringify(tasks)
        );


        renderTasks(tasks);


    } catch(error) {

        console.log("Error loading tasks:", error);

    }


// Tasks ko screen par show karna

function renderTasks(taskList) {


    const container = document.getElementById("tasks");


    container.innerHTML = "";


    taskList.forEach(task => {


        const taskDiv = document.createElement("div");

        taskDiv.className = "task-item";



        const title = document.createElement("h3");

        title.textContent = task.title;



        const description = document.createElement("p");

        description.textContent = task.description || "";



        const priority = document.createElement("p");

        priority.textContent =
            `Priority: ${task.priority}`;



        const status = document.createElement("p");

        status.textContent =
            `Status: ${task.status}`;



        const editButton = document.createElement("button");

        editButton.textContent = "Edit";


        editButton.addEventListener(
            "click",
            () => editTask(task)
        );



        const deleteButton = document.createElement("button");

        deleteButton.textContent = "Delete";


        deleteButton.addEventListener(
            "click",
            () => deleteTask(task.id)
        );



        taskDiv.appendChild(title);

        taskDiv.appendChild(description);

        taskDiv.appendChild(priority);

        taskDiv.appendChild(status);

        taskDiv.appendChild(editButton);

        taskDiv.appendChild(deleteButton);



        container.appendChild(taskDiv);


    });


}


// ADD TASK

document
.getElementById("taskForm")
.addEventListener(
    "submit",
    async function(event) {


        event.preventDefault();



        const titleInput =
            document.getElementById("title");



        const title =
            titleInput.value.trim();



        const error =
            document.getElementById("titleError");



        if(title === "") {


            error.textContent =
                "Title cannot be empty";


            return;

        }


        error.textContent = "";



        const taskData = {


            title: title,

            description:
                document.getElementById("description").value,


            priority:
                document.getElementById("priority").value,


            status:
                document.getElementById("status").value,


            due_date:
                document.getElementById("due_date").value,


            project_id:
                Number(document.getElementById("project").value)


        };



        const response =
            await fetch(
                `${API_URL}/tasks`,
                {

                    method:"POST",

                    headers:{
                        "Content-Type":"application/json"
                    },

                    body:
                        JSON.stringify(taskData)

                }
            );


        if(response.ok){

            document
            .getElementById("taskForm")
            .reset();


            fetchTasks();

        }



    }
);



// DELETE TASK

async function deleteTask(id){


    await fetch(
        `${API_URL}/tasks/${id}`,
        {
            method:"DELETE"
        }
    );


    fetchTasks();


}


// EDIT TASK

function editTask(task){


    document.getElementById("editSection")
    .style.display="block";


    document.getElementById("editTitle").value =
        task.title;


    document.getElementById("editDescription").value =
        task.description;


    document.getElementById("editPriority").value =
        task.priority;


    document.getElementById("editStatus").value =
        task.status;


    document.getElementById("editDueDate").value =
        task.due_date;


    window.currentTaskId = task.id;
    window.currentProjectId = task.project_id;


}


// SAVE EDIT

document
.getElementById("editForm")
.addEventListener(
"submit",
async function(event){


    event.preventDefault();



    const updatedTask = {

    title:
    document.getElementById("editTitle").value.trim(),

    description:
    document.getElementById("editDescription").value,

    priority:
    document.getElementById("editPriority").value,

    status:
    document.getElementById("editStatus").value,

    due_date:
    document.getElementById("editDueDate").value,

    project_id:
    window.currentProjectId

};


    await fetch(
        `${API_URL}/tasks/${window.currentTaskId}`,
        {

            method:"PUT",

            headers:{
                "Content-Type":"application/json"
            },

            body:
            JSON.stringify(updatedTask)

        }
    );



    document.getElementById("editSection")
    .style.display="none";


    fetchTasks();


});