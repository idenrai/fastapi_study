<!-- 
    error를 전달받아 오류를 표시
 -->
<script>
  // 전달받은 에러의 속성 지정
  export let error
</script>

{#if typeof error.detail === 'string'}
  <ul>
    <li>{error.detail}</li>
  </ul>
{:else if typeof error.detail === 'object' && error.detail.length > 0}
  <ul>
    {#each error.detail as err, i}
      <li>
        <strong>{err.loc[1]}</strong> : {err.msg}
      </li>
    {/each}
  </ul>
{/if}
