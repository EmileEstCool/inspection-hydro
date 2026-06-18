async function uploadFile() {

    const fileInput = document.getElementById("fileInput");

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    const list = document.getElementById("checklist");
    list.innerHTML = "";

    data.tasks.forEach(t => {
        const li = document.createElement("li");
        li.innerText = t.task;
        list.appendChild(li);
    });
}
