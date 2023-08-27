import { Fragment, useEffect, useState } from 'react';
import Introduction from './Introduction';
import axios from 'axios';
import algorithmType from './constant';

function App() {
  const BASE_URL = 'https://group-formation.herokuapp.com/';
  // const BASE_URL = 'http://localhost:5000';
  const DOWNLOAD_FILE_NAME = 'result.csv';

  const [file, setFile] = useState(null);
  const [groupNum, setGroupNum] = useState(2);
  const [uuid, setUuid] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [algorithm, setAlgorithm] = useState(algorithmType.geneticAlgorithm);

  const submitHandler = (event) => {
    event.preventDefault();
    const fd = new FormData();
    fd.append('file', file);
    fd.append('group_num', groupNum);
    fd.append('algorithm_type', algorithm);
    setLoading(true);
    axios.post(BASE_URL + '/upload', fd).then((res) => {
      setUuid(res.data.uuid);
      setFile(null);
    })
      .catch((error) => {
      setLoading(false);
      setFile(null);
      setError(error.response.data);
    });
  };

  const algorithmTypeHandler = (event) => {
    setAlgorithm(event.target.value);
  }

  const fileSelectedHandler = (event) => {
    setFile(event.target.files[0]);
  };

  const inputGroupNumHandler = (event) => {
    setGroupNum(event.target.value);
  };

  useEffect(() => {
    let timer = null;
    if (uuid && !timer) {
      timer = setInterval(() => {
        axios
          .post(BASE_URL + '/check', {
            uuid,
          })
          .then((response) => {
            if (response.status === 200) {
              if (response.data.startsWith('error')) {
                setError(response.data);
              } else {
                var blob = new Blob([response.data], { type: 'text/csv' });
                //Create a link element, hide it, direct
                //it towards the blob, and then 'click' it programatically
                let a = document.createElement('a');
                a.style = 'display: none';
                document.body.appendChild(a);
                //Create a DOMString representing the blob
                //and point the link element towards it
                let url = window.URL.createObjectURL(blob);
                a.href = url;
                a.download = DOWNLOAD_FILE_NAME;
                //programatically click the link to trigger the download
                a.click();
                //release the reference to the file by revoking the Object URL
                window.URL.revokeObjectURL(url);
              }
              clearInterval(timer);
              setLoading(false);
            } else if (response.status === 202) {
              console.log(response.data);
            }
          })
          .catch((reason) => {
            console.log(reason);
          });
      }, 5000);
    } else if (!uuid && timer) {
      clearInterval(timer);
    }

    return () => {
      if (timer) {
        clearInterval(timer);
      }
    };
  }, [uuid]);

  const errorCard = (
    <div className="errorCard">
      <h3 style={{ color: 'red' }}>Forming groups failed.</h3>
      <p>{error}</p>
      <button onClick={() => { setError(null); }} >{' OK '}</button>
    </div>
  );

  const content = (
    <div id="content">
      <form onSubmit={submitHandler}>
        <span>Choose Algorithm: </span>
        <label>
          <input
            type="radio"
            onChange={algorithmTypeHandler}
            value={algorithmType.geneticAlgorithm}
            checked={algorithm === algorithmType.geneticAlgorithm}
          />
          Genetic Algorithm
        </label>
        <label>
          <input
            type="radio"
            onChange={algorithmTypeHandler}
            value={algorithmType.KMeans}
            checked={algorithm === algorithmType.KMeans}
          />
          K-means Clustering Algorithm
        </label>
        <br />
        <label>Group Number: </label>
        <input
          type="number"
          onChange={inputGroupNumHandler}
          value={groupNum}
          min="2"
        />
        <br />
        <input type="file" onChange={fileSelectedHandler} />
        <br />
        <input type="submit" value="Submit" disabled={!file} />
      </form>
    </div>
  );

  const loadingCard = (
    <div id="loader">
      <div> Processing.... It will take half to a few minutes.</div>
      <div>
        Please do <b>NOT</b> close or refresh this page.
      </div>
      <div className="loading"></div>
    </div>
  );

  return (
    <Fragment>
      <div className="container">
        <Introduction />
        <main>
          <h2>4. Upload csv file</h2>
          {loading ? loadingCard : error ? errorCard : content}
        </main>
      </div>
    </Fragment>
  );
}

export default App;
