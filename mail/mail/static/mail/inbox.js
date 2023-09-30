document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector("#details-view").style.display = "none";

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#details-view").style.display = "none";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    //creando la estructura que tendra cada uno de los emailss 
    emails.forEach(singleEmail => {
      console.log(singleEmail);
      const newEmail= document.createElement("div");
      newEmail.className = "list-group-item";
      newEmail.innerHTML = `
      <h5>Sender: ${singleEmail.sender}</h5>
      <h5>Subject: ${singleEmail.subject}</h5>
      <p>Timestamp: ${singleEmail.timestamp}</p>

      `;
      //cambiar el color de los emails que no han sido leidos
      newEmail.className = singleEmail.read ? 'read': 'unread';

      newEmail.addEventListener("click", function(){
       view_email(singleEmail)
      }) 
      document.querySelector("#details-view").innerHTML = "";
      document.querySelector("#emails-view").append(newEmail);
    })
  });
}


//seleccionar el DOM y darle asignarle un atributo al boton del formulario
function send_email(event) {
  event.preventDefault();
    const recipients= document.querySelector("#compose-recipients").value;
    const subject= document.querySelector("#compose-subject").value;
    const body= document.querySelector("#compose-body").value;
    fetch('/emails', {
      method: "POST",
      body: JSON.stringify({
        recipients:recipients,
        subject:subject,
        body:body
      })
    })
    .then(responde => responde.json())
    .then(result => {
      console.log(result)
      load_mailbox("sent")
    })
}
document.addEventListener("DOMContentLoaded", function(){
  document.querySelector("#compose-form").onsubmit = send_email 
    
});


function view_email(email) {
  fetch (`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector("#details-view").style.display = "block";
      const details= document.createElement("div");
      details.className = "list-group-item";
      details.innerHTML = `
      <h5>Sender: ${email.sender}</h5>
      <h6>Recipients: ${email.recipients}</h6>
      <p>Subject: ${email.subject}</p>
      <p>TimeStamp: ${email.timestamp}
      <p>Body: ${email.body}</p>
      `;
      document.querySelector("#details-view").append(details)
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
      const reply = document.createElement('button');
      reply.innerHTML = "reply";
      reply.className = "btn btn-success";
      
      reply.addEventListener('click', function() {
        compose_email()
        let subject = email.subject
        if(subject.split(" ",1)[0] != "Re:"){
          subject = "Re: " + email.subject;
        }
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} write: ${email.body}`;
      });
      document.querySelector('#details-view').append(reply);
      const element = document.createElement('button');
      element.innerHTML = email.archived ? "Unarchive": "Archive";
      element.className = email.archived ? "btn btn-success": "btn btn-danger";
      element.addEventListener('click', function() {
        add_archive(email)
      });
      document.querySelector('#details-view').append(element);
    });
      
}

// agregando o desagregando a archived
function add_archive(email){
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  })
  .then (() => {load_mailbox("inbox")})
};



