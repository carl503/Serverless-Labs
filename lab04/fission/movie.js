const template = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Recommender - Fission version</title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
    
</head>
<body>

    <div class="container">

        <section class="hero is-info">
            <div class="hero-body">
                <p class="title">
                    Movie Recommender - Fission version
                </p>
                <p class="subtitle">
                    SCAD: albreaus, meletlea, lubojcar
                </p>
            </div>
        </section>

        <div class="recommendForm">
            <div class="field">
                <label class="label">Username</label>
                <div class="control">
                    <input class="input" type="text" id="username" placeholder="Carl">
                </div>
            </div>
    
    
            <div class="field">
                <label class="label">Movie</label>
                <div class="control">
                    <div class="select">
                    <select name="movies" id="movieSelect">
                
                    </select>
                    </div>
                </div>
            </div>
    
            <div class="field">
                <label class="label">Rating</label>
                <div class="control">
                    <input class="input" type="number" name="rating" id="rating" min="0" max="10" step="0.5" placeholder="5">
                </div>
            </div>
    
            <div class="field">
                <div class="control">
                  <button class="button is-link" onclick="submitForm()" id="submitBtn">Submit</button>
                </div>
              </div>
    
        </div>
    
        <div id="output">
            <table class="table is-striped">
                <thead>
                    <tr>
                        <th>Recommended Movies</th>
                    </tr>
                </thead>
                <tbody id="tableContent">
    
                </tbody>
            </table>
        </div>
    </div>


    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script>
        const recommendAPIBase = "https://nt0xeiu3x8.execute-api.eu-central-1.amazonaws.com/api"


        function submitForm() {

            const username = $("#username").val()
            const movie = $("#movieSelect").val()
            const rating = $("#rating").val()
            const data = {
                movieID: movie,
                user: username,
                rating: rating
            }
        
            console.log(\`Submitting: \`, data)
            $("#submitBtn").prop("disabled", true)
            $("#submitBtn").addClass("is-loading")
        
            fetch(\`\${recommendAPIBase}/recommendation\`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.text())
            .then(data => {
        
                let invervalID = setInterval(() => {
                    
                    fetch(\`\${recommendAPIBase}/recommendation/status/\${data}\`)
                    .then(response => response.json())
                    .then(d => {
                        if(d.state === "succeeded") {
                            clearInterval(invervalID);
                            console.log('Success:', d)
                            d.data = JSON.parse(d.data)
                            for (let i = 0; i < d.data.length; i++) {
                                $("#tableContent").append(\`<tr><td>\${d.data[i]}</td></tr>\`)
                            }
                            $("#submitBtn").prop("disabled", false)
                            $("#submitBtn").removeClass("is-loading")
                        } else if (d.state === "failed") {
                            console.error("What the fuck");
                            clearInterval(invervalID);
                        }
                    })
                }, 2000);
                
            })
        }

        function setupMovieOptions() {

            console.log("Fetching movies");

            fetch(\`\${recommendAPIBase}/movies\`)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                
                    for (let i = 0; i < data.length; i++) {
                        data[i];
                        $("#movieSelect").append(\`<option value="\${data[i].id}">\${data[i].title}</option>\`)
                    }
                })

        }


        setupMovieOptions()
    </script>

</body>
</html>
`

module.exports = async function(context) {
    return {
        status: 200,
        body: template
    };
}
