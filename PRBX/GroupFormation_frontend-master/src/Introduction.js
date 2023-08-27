function Introduction() {
  return (
    <div>
      <h1 className="title">Group Formation Online Tool</h1>

      <h2>1. Introduction</h2>
      <p>
        This website is an online tool that can divide a group of people into a
        set of balanced groups. Forming groups is a complex and time-consuming
        task, which is hard to be achieved by linear search. Therefore, this
        tool is based on algorithms that can give an ideal solution
        within limited time.
      </p>
      <h2>2. How to use</h2>
      <ol>
        <li>Choose an algorithm that you want to use.</li>
        <li>Input the group number that people need to be divdied into.</li>
        <li>
          Upload a csv file containig all people's information. csv file should
          follow the style showed in the below table. The first row should be
          title: ID, C1, C2, C3...., which will be <b>skipped </b>when processing.
        </li>
        <li>ID can be integer or string. ID need be to unique.</li>
        <li>
          C1, C2, C3... stand for characteristics that need be integers or
          decimals. They can be students' grades, gender, or any kinds of metrics
          of their performance.
        </li>
        <li>
          After submiting, the backend server will process the uploaded csv
          file. It will take half to a few minutes. After that, a new csv
          file containing group formation information will be downloaded as an
          attachment.
        </li>
      </ol>
      <table>
        <tbody>
          <tr>
            <th>ID</th>
            <th>C1</th>
            <th>C2</th>
            <th>C3</th>
            <th>...</th>
          </tr>
          <tr>
            <td>1</td>
            <td>0.1</td>
            <td>3</td>
            <td>24</td>
            <td>...</td>
          </tr>
          <tr>
            <td>2</td>
            <td>0.4</td>
            <td>6</td>
            <td>57</td>
            <td>...</td>
          </tr>
          <tr>
            <td>3</td>
            <td>0.7</td>
            <td>11</td>
            <td>87</td>
            <td>...</td>
          </tr>
          <tr>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
            <td>...</td>
          </tr>
        </tbody>
      </table>

      <h2>3. Note</h2>
      <ol>
        <li>
          ID must be <b>unique</b>.
        </li>
        <li>
          Group number need to be <b>at least 2</b>, and it must be{' '}
          <b>divisble by total people number</b>. Total people number need to
          be <b>at least 4</b>.
        </li>
        <li>
          There can be any number of characteristics but <b>at least 1</b>.
        </li>
        <li>
          There must <b>NOT</b> be a column where all people's characteristics
          are the <b>same</b>.
        </li>
        <li>
          Please use Chrome, Firefox or IE browser.{' '}
          <b style={{ color: 'red' }}>Safari won't work.</b>
        </li>
      </ol>
    </div>
  );
}

export default Introduction;
