<script>
  let question_list = []

  function get_question_list() {
    fetch('http://127.0.0.1:8000/api/question/list').then(response => {
      response.json().then(json => {
        question_list = json
      })
    })
  }

  get_question_list()
</script>

<ul>
  {#each question_list as question}
    <li>
      <div>
        <p>제목 : {question.subject}</p>
        <p>내용 : {question.content}</p>
      </div>
    </li>
  {/each}
</ul>
