const API_URL =
    "http://127.0.0.1:8000/environment/analyze";


// =====================================================
// SESSION
// =====================================================

let sessionId =
    localStorage.getItem("ecomind_session_id");

if (!sessionId) {

    sessionId =
        "session_" +
        Date.now();

    localStorage.setItem(
        "ecomind_session_id",
        sessionId
    );
}


// =====================================================
// DOM ELEMENTS
// =====================================================

const analyzeButton =
    document.getElementById(
        "analyzeButton"
    );

const chatAnalyzeButton =
    document.getElementById(
        "chatAnalyzeButton"
    );

const results =
    document.getElementById(
        "results"
    );


// =====================================================
// HELPER FUNCTIONS
// =====================================================

function getValue(id) {

    const element =
        document.getElementById(id);

    if (!element) {
        return null;
    }

    const value =
        element.value.trim();

    return value === ""
        ? null
        : value;
}


function getNumber(id) {

    const value =
        getValue(id);

    if (
        value === null ||
        value === ""
    ) {
        return null;
    }

    const number =
        Number(value);

    return Number.isNaN(number)
        ? null
        : number;
}


function escapeHtml(value) {

    if (value === null ||
        value === undefined) {

        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// =====================================================
// BUILD REQUEST
// =====================================================

function buildRequest(message) {

    return {

        session_id: sessionId,

        message: message,

        region:
            getValue("region"),

        latitude:
            getNumber("latitude"),

        longitude:
            getNumber("longitude"),

        soil_ph:
            getNumber("soil_ph"),

        soil_organic_carbon:
            getNumber(
                "soil_organic_carbon"
            ),

        soil_moisture:
            getNumber(
                "soil_moisture"
            ),

        land_use:
            getValue("land_use"),

        species_richness:
            getNumber(
                "species_richness"
            ),

        habitat_diversity:
            getNumber(
                "habitat_diversity"
            ),

        temperature:
            getNumber(
                "temperature"
            ),

        rainfall:
            getNumber(
                "rainfall"
            ),

        pollution:
            getValue("pollution"),

        deforestation:
            getValue("deforestation")
    };
}


// =====================================================
// DISPLAY MESSAGE
// =====================================================

function addUserMessage(message) {

    results.innerHTML += `

        <div class="message user-message">

            <strong>You:</strong>

            <p>
                ${escapeHtml(message)}
            </p>

        </div>

    `;
}


function addLoadingMessage() {

    results.innerHTML += `

        <div class="message ecomind-message">

            <strong>EcoMind:</strong>

            <p>
                Analyzing your environment...
            </p>

        </div>

    `;
}


// =====================================================
// ANALYZE ENVIRONMENT
// =====================================================

async function analyzeEnvironment() {

    const message =
        getValue("message") ||
        getValue("chatMessage");

    if (!message) {

        alert(
            "Please describe your environmental problem first."
        );

        return;
    }


    addUserMessage(message);

    addLoadingMessage();


    try {

        const requestData =
            buildRequest(message);


        console.log(
            "EcoMind request:",
            requestData
        );


        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            requestData
                        )
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "EcoMind response:",
            data
        );


        // Remove loading message
        const messages =
            results.querySelectorAll(
                ".ecomind-message"
            );

        if (messages.length > 0) {

            messages[
                messages.length - 1
            ].remove();
        }


        displayResponse(data);

    }

    catch (error) {

        console.error(
            "EcoMind error:",
            error
        );


        const messages =
            results.querySelectorAll(
                ".ecomind-message"
            );

        if (messages.length > 0) {

            messages[
                messages.length - 1
            ].remove();
        }


        results.innerHTML += `

            <div class="message error-message">

                <strong>EcoMind:</strong>

                <p>
                    Unable to connect to the
                    EcoMind backend.
                </p>

                <p>
                    Please make sure FastAPI
                    is running on
                    <strong>
                        127.0.0.1:8000
                    </strong>
                </p>

            </div>

        `;
    }
}


// =====================================================
// DISPLAY RESPONSE
// =====================================================

function displayResponse(data) {

    if (
        data.status ===
        "needs_more_information"
    ) {

        displayClarification(
            data
        );

        return;
    }


    if (
        data.status !==
        "analysis_complete"
    ) {

        results.innerHTML += `

            <div class="message ecomind-message">

                <strong>EcoMind:</strong>

                <p>
                    ${escapeHtml(
                        data.message ||
                        "Analysis completed."
                    )}
                </p>

            </div>

        `;

        return;
    }


    let html = `

        <div class="message ecomind-message">

            <strong>EcoMind:</strong>

            <p>
                Your environmental profile has
                been analyzed using multi-metric
                reasoning and retrieved scientific
                evidence.
            </p>

    `;


    // =================================================
    // PROBLEM
    // =================================================

    if (data.problem) {

        html += `

            <p>
                <strong>
                    Environmental problem:
                </strong>

                ${escapeHtml(
                    data.problem
                )}
            </p>

        `;
    }


    // =================================================
    // RECOMMENDATIONS
    // =================================================

    if (
        !data.recommendations ||
        data.recommendations.length === 0
    ) {

        html += `

            <p>
                No recommendation was generated
                for the current environmental
                profile.
            </p>

        `;

    } else {

        data.recommendations.forEach(
            (recommendation, index) => {

                html += `

                    <div class="recommendation-card">

                        <h2>
                            🌿 Recommendation
                            ${index + 1}
                        </h2>


                        <p>
                            <strong>
                                What to do:
                            </strong>
                        </p>

                        <p>
                            ${escapeHtml(
                                recommendation.recommendation
                            )}
                        </p>


                        <p>
                            <strong>
                                Why it works:
                            </strong>
                        </p>

                        <p>
                            ${escapeHtml(
                                recommendation.reasoning
                            )}
                        </p>


                        <p>
                            <strong>
                                Impacted metrics:
                            </strong>
                        </p>

                        <ul>
                `;


                if (
                    recommendation.impacted_metrics
                ) {

                    recommendation
                        .impacted_metrics
                        .forEach(metric => {

                            html += `

                                <li>
                                    ${escapeHtml(
                                        metric
                                    )}
                                </li>

                            `;

                        });
                }


                html += `

                        </ul>


                        <p>

                            <strong>
                                Time horizon:
                            </strong>

                            ${escapeHtml(
                                recommendation.time_horizon
                            )}

                        </p>


                        <p>

                            <strong>
                                Confidence:
                            </strong>

                            ${escapeHtml(
                                recommendation.confidence
                            )}

                            ${
                                recommendation
                                    .confidence_score !==
                                undefined
                                    ? `(${recommendation.confidence_score})`
                                    : ""
                            }

                        </p>

                `;


                // =====================================
                // MEASUREMENT PLAN
                // =====================================

                if (
                    recommendation.measurement_plan
                ) {

                    const plan =
                        recommendation
                            .measurement_plan;


                    html += `

                        <div class="measurement-plan">

                            <p>
                                <strong>
                                    📊 Measurement &
                                    Monitoring Plan
                                </strong>
                            </p>


                            <p>
                                <strong>
                                    Baseline metrics:
                                </strong>
                            </p>

                            <ul>

                    `;


                    if (
                        plan.baseline_metrics
                    ) {

                        plan
                            .baseline_metrics
                            .forEach(metric => {

                                html += `

                                    <li>
                                        ${escapeHtml(
                                            metric
                                        )}
                                    </li>

                                `;

                            });
                    }


                    html += `

                            </ul>


                            <p>

                                <strong>
                                    Monitoring frequency:
                                </strong>

                                ${escapeHtml(
                                    plan.monitoring_frequency
                                )}

                            </p>


                            <p>
                                <strong>
                                    Expected direction:
                                </strong>
                            </p>

                            <ul>

                    `;


                    if (
                        plan.expected_direction
                    ) {

                        Object.entries(
                            plan.expected_direction
                        ).forEach(
                            ([metric, direction]) => {

                                html += `

                                    <li>

                                        ${escapeHtml(
                                            metric
                                        )}

                                        →

                                        ${escapeHtml(
                                            direction
                                        )}

                                    </li>

                                `;

                            }
                        );
                    }


                    html += `

                            </ul>


                            <p>

                                <strong>
                                    Biodiversity indicator:
                                </strong>

                                ${escapeHtml(
                                    plan.biodiversity_indicator
                                )}

                            </p>

                        </div>

                    `;
                }


                // =====================================
                // QUANTITATIVE EVIDENCE
                // =====================================

                if (
                    recommendation
                        .quantitative_evidence &&
                    recommendation
                        .quantitative_evidence
                        .length > 0
                ) {

                    html += `

                        <div class="quantitative-evidence">

                            <h3>
                                📈 Quantitative
                                Scientific Evidence
                            </h3>

                            <p>
                                These estimates are
                                reported by scientific
                                studies/meta-analyses.
                                They are not guaranteed
                                predictions for this
                                specific site.
                            </p>

                    `;


                    recommendation
                        .quantitative_evidence
                        .forEach(
                            evidence => {

                                html += `

                                    <div class="evidence-card">

                                        <p>
                                            <strong>
                                                Metric:
                                            </strong>

                                            ${escapeHtml(
                                                evidence.metric
                                            )}
                                        </p>


                                        <p>
                                            <strong>
                                                Reported estimate:
                                            </strong>

                                            ${escapeHtml(
                                                evidence.estimate
                                            )}
                                        </p>


                                        <p>
                                            <strong>
                                                Evidence type:
                                            </strong>

                                            ${escapeHtml(
                                                evidence.estimate_type
                                            )}
                                        </p>


                                        <p>
                                            <strong>
                                                Practice:
                                            </strong>

                                            ${escapeHtml(
                                                evidence.practice
                                            )}
                                        </p>


                                        <p>
                                            <strong>
                                                Conditions:
                                            </strong>

                                            ${escapeHtml(
                                                evidence.conditions
                                            )}
                                        </p>


                                        <p>
                                            <strong>
                                                Scientific source:
                                            </strong>

                                            ${escapeHtml(
                                                evidence.source_title
                                            )}

                                            ${
                                                evidence.organization
                                                    ? ` - ${escapeHtml(
                                                        evidence.organization
                                                    )}`
                                                    : ""
                                            }

                                        </p>


                                        ${
                                            evidence.url
                                                ? `

                                                    <p>

                                                        <strong>
                                                            Source:
                                                        </strong>

                                                        <a
                                                            href="${escapeHtml(
                                                                evidence.url
                                                            )}"
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                        >
                                                            View scientific study
                                                        </a>

                                                    </p>

                                                `
                                                : ""
                                        }

                                    </div>

                                `;

                            }
                        );


                    html += `

                        </div>

                    `;
                }


                // =====================================
                // SCIENTIFIC EVIDENCE
                // =====================================

                if (
                    recommendation.evidence &&
                    recommendation.evidence.length > 0
                ) {

                    html += `

                        <div class="scientific-evidence">

                            <h3>
                                📚 Scientific evidence
                            </h3>

                    `;


                    recommendation.evidence
                        .forEach(item => {

                            const source =
                                item.scientific_source;


                            html += `

                                <div class="evidence-card">

                            `;


                            if (source) {

                                html += `

                                    <h4>

                                        ${escapeHtml(
                                            source.title
                                        )}

                                        ${
                                            source.organization
                                                ? ` - ${escapeHtml(
                                                    source.organization
                                                )}`
                                                : ""
                                        }

                                    </h4>

                                `;
                            }


                            html += `

                                    <p>

                                        <strong>
                                            Relevance:
                                        </strong>

                                        ${escapeHtml(
                                            item.relevance_score
                                        )}

                                    </p>


                                    <p>
                                        ${escapeHtml(
                                            item.supporting_text
                                        )}
                                    </p>

                            `;


                            if (
                                source &&
                                source.url
                            ) {

                                html += `

                                    <p>

                                        <strong>
                                            Source:
                                        </strong>

                                        <a
                                            href="${escapeHtml(
                                                source.url
                                            )}"
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            View scientific source
                                        </a>

                                    </p>

                                `;
                            }


                            html += `

                                </div>

                            `;

                        });


                    html += `

                        </div>

                    `;
                }


                html += `

                    </div>

                `;
            }
        );
    }


    html += `

        </div>

    `;


    results.innerHTML += html;


    // Scroll to newest response
    results.scrollTop =
        results.scrollHeight;
}


// =====================================================
// CLARIFICATION QUESTIONS
// =====================================================

function displayClarification(data) {

    let html = `

        <div class="message ecomind-message">

            <strong>EcoMind:</strong>

            <p>
                I need a little more environmental
                information before making a
                recommendation.
            </p>

            <p>
                <strong>
                    Please provide:
                </strong>
            </p>

            <ul>

    `;


    if (data.questions) {

        data.questions.forEach(
            question => {

                html += `

                    <li>
                        ${escapeHtml(
                            question
                        )}
                    </li>

                `;

            }
        );
    }


    html += `

            </ul>

        </div>

    `;


    results.innerHTML += html;
}


// =====================================================
// BUTTON EVENTS
// =====================================================

if (analyzeButton) {

    analyzeButton.addEventListener(
        "click",
        analyzeEnvironment
    );
}


if (chatAnalyzeButton) {

    chatAnalyzeButton.addEventListener(
        "click",
        analyzeEnvironment
    );
}


// =====================================================
// ENTER KEY SUPPORT
// =====================================================

const messageBox =
    document.getElementById(
        "message"
    );

if (messageBox) {

    messageBox.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter" &&
                event.ctrlKey
            ) {

                analyzeEnvironment();

            }

        }
    );
}