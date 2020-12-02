document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // add submit event listener
  const form = document.getElementById("compose-form");
  form.addEventListener('submit', post_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {


  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  if (mailbox === 'sent') {
    get_sent();
  };
  //get_mailbox(mailbox);

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function post_email() {

  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;


  fetch('http://127.0.0.1:8000/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json());
};

function get_sent() {

  fetch('http://127.0.0.1:8000/emails/sent')
  .then(res => res.json())
  .then(sent_emails => {
    // Each email should then be rendered in its own box (e.g. as a <div> with a border) that displays who the email is from, what the subject line is, and the timestamp of the email.

    let emails_div = document.querySelector('#emails-view');

    sent_emails.forEach(email => {

      const sender = document.createElement('b');
      sender.innerHTML = email['sender'];
      sender.style.display = "inline-block";
      sender.style.padding = "8px";
      sender.style.marginTop = "auto";
      sender.style.marginBottom = "auto";

      const subject = document.createElement('p');
      subject.innerHTML = email['subject'];
      subject.style.display = "inline-block";
      subject.style.padding = "8px";
      subject.style.marginTop = "auto";
      subject.style.marginBottom = "auto";


      const timestamp = document.createElement('p');
      timestamp.innerHTML = email['timestamp'];
      timestamp.style.display = "inline-block";
      timestamp.style.padding = "8px";
      timestamp.style.marginTop = "auto";
      timestamp.style.marginBottom = "auto";
      timestamp.style.marginLeft = "auto";
      timestamp.style.color = "grey";

      let email_container = document.createElement('div');
      email_container.style.border = "solid 1px";
      email_container.style.display = "flex";
      email_container.style.padding = "6px";


      //email_container.innerHTML = `${sender}  ${subject}  ${timestamp}`;
      email_container.append(sender, subject, timestamp);
      emails_div.append(email_container);
    });
  });
};