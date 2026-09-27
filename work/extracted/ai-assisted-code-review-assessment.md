---
source_file: "data/materials/CS146S_offline/pdfs/ai-assisted-code-review-assessment.pdf"
origin_url: ""
title: "AI-Assisted Assessment of Coding Practices"
extract_method: "pdf"
extract_warnings:
  - "UNDECODED_CODES：有 1910 个字符码在对应字体的 CMap 里找不到映射，已按纪律留空，未做任何猜测补全。（Type3/字体子集未提供完整 ToUnicode 时会发生）"
src_sha256: "e1c71b8058d1521f0cf6c0537ae00934fcc075c65b5aa69b26539baf3bcc3f4b"
chars: 51829
code_blocks: 0
tables: 0
links: 16
garbage_rate: 0.0309
pdf_type: "text"
bt_operators: 92
fonts_total: 34
fonts_with_basefont: 20
readable_line_ratio: 0.4186
---

# AI-Assisted Assessment of Coding Practices

AI-Assisted Assessment of Coding Practices

in Modern Code Review

Manushree Vijayvergiya

manushree@google.com

Google

Zurich, Switzerland

Małgorzata Salawa

magorzata@google.com

Google

Zurich, Switzerland

Ivan Budiselić

ibudiselic@google.com

Google

Zurich, Switzerland

Dan Zheng

danielzheng@google.com

Google

Mountain View, USA

Pascal Lamblin

lamblinp@google.com

Google

Montreal, Canada

Marko Ivanković

markoi@google.com

Google

Zurich, Switzerland

Juanjo Carin

juanjocarin@google.com

Google

Sunnyvale, USA

Mateusz Lewko

mlewko@google.com

Google

Zurich, Switzerland

Jovan Andonov

jandonov@google.com

Google

Zurich, Switzerland

Goran Petrovićgoranpetrovic@google.comGoogle

Zurich, Switzerland

Daniel Tarlow

dtarlow@google.com

Google

Montreal, Canada

Petros Maniatis

maniatis@google.com

Google

Mountain View, USA

René Just

∗

rjust@cs.washington.edu

University of Washington

Seattle, USA

ABSTRACTModern code review is a process in which an incremental code con-tribution made by a code author is reviewed by one or more peersbefore it is committed to the version control system. An importantelement of modern code review is verifying that code contributionsadhere to best practices. While some of these best practices can beautomatically verified, verifying others is commonly left to humanreviewers. This paper reports on the development, deployment,and evaluation of AutoCommenter, a system backed by a largelanguage model that automatically learns and enforces coding bestpractices. We implemented AutoCommenter for four programminglanguages (C++, Java, Python, and Go) and evaluated its perfor-mance and adoption in a large industrial setting. Our evaluationshows that an end-to-end system for learning and enforcing codingbest practices is feasible and has a positive impact on the devel-oper workflow. Additionally, this paper reports on the challengesassociated with deploying such a system to tens of thousands ofdevelopers and the corresponding lessons learned.

CCS CONCEPTS•Software and its engineering→Software verification andvalidation

.

∗

Work done at Google.

Permission to make digital or hard copies of all or part of this work for personal orclassroom use is granted without fee provided that copies are not made or distributedfor profit or commercial advantage and that copies bear this notice and the full citationon the first page. Copyrights for third-party components of this work must be honored.For all other uses, contact the owner/author(s).

AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

©

2024 Copyright held by the owner/author(s).

ACM ISBN 979-8-4007-0685-1/24/07

https://doi.org/10.1145/3664646.3665664

KEYWORDS

Artificial Intelligence, Code Review, Coding Best Practices

ACM Reference Format:

Manushree Vijayvergiya, Małgorzata Salawa, Ivan Budiselić, Dan Zheng,Pascal Lamblin, Marko Ivanković, Juanjo Carin, Mateusz Lewko, Jovan An-donov, Goran Petrović, Daniel Tarlow, Petros Maniatis, and René Just. 2024.AI-Assisted Assessment of Coding Practices in Modern Code Review. InProceedings of the 1st ACM International Conference on AI-Powered Software(AIware ’24), July 15–16, 2024, Porto de Galinhas, Brazil.ACM, New York,NY, USA, 9 pages. https://doi.org/10.1145/3664646.3665664

1 INTRODUCTIONModern code review [21,238has grown organically over the years in open-source and industrialsettings. A set of common peer-review criteria have emerged [5,20,21and even programming languages formally define them in the formof “style guides” [1–4•Formatting: line limits, use of whitespaces and indentation,placement of parentheses and brackets, etc.;

•

Naming

: capitalization, brevity, descriptiveness, etc.;

•Documentation: expected placement and content of file-level,function-level, and other comments;

•Language features: use of specific language features in differ-ent (code) contexts;

•Code idioms: use of code idioms to improve code clarity,modularity, and maintainability.Developers generally report high satisfaction with modern codereview processes [23,28experience for code authors who are not familiar with the codebase,specific language features, or common code idioms. During a review,an expert developer educates the code author on best practices, in

arXiv:2405.13565v1  [cs.SE]  22 May 2024

AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

Manushree Vijayvergiya et al.addition to reviewing (and learning about) the code contributionsand their implications.Static analysis tools such as linters [15that code adheres to some best practices (e.g., formatting rules), andsome tools can even automatically fix violations. However, nuancedguidelines or those with exceptions are difficult to automaticallyverify in their entirety (e.g., naming conventions and justified devi-ations in legacy code), and some guidelines cannot be captured byprecise rules at all (e.g., clarity and specificity of code comments)and rely on human judgement and collective developer knowledge.As a result, it is generally expected that human reviewers checkcode changes for best practice violations.The biggest cost of the code-review process is the time required,especially from expert developers. Even with significant automa-tion in place, and keeping the process as lightweight as possible, adeveloper can easily dedicate several hours daily to this task [23Recent advances in machine learning, capabilities of large lan-guage models (LLMs) in particular, suggest that LLMs are suitablefor code-review automation (e.g., [11,16,17,24–26software engineering challenges around deploying an end-to-endsystem at scale remain unexplored. Likewise, extrinsic evaluationsof such systems on overall efficacy and user acceptance are missing.This paper investigates whether it is possible to partially au-tomate the code-review process, specifically the detection of bestpractice violations, thereby providing timely feedback for codeauthors and allowing reviewers to focus on overall functionality.Specifically, this paper reports on our experience of developing,deploying, and evaluating AutoCommenter—an automated code-review assistant—in an industrial setting at Google, where it iscurrently used by tens of thousands of developers every day.

In summary, the contributions of this paper are:

•A general architecture of an LLM-based code-review assis-tant system (section 3).

•A description of tool calibration and deployment to tens ofthousands of developers (section 4).

•

An evaluation of the system (section 5).

•

A summary and discussion of lessons learned (section 6).

2 BACKGROUNDAutoCommenter was developed in a large industrial setting atGoogle. The modern code review practices at Google are similar tothose of other industrial and open source projects [23

2.1 Code Review ProcessThe code review process at Google is well established, change-based, and tool-assisted. Ivanković et al. [12and Petrović et al.

[18provide a detailed summary of the process. Each change to thecodebase must be reviewed by at least one other developer. Everyday, tens of thousands of changes to the codebase go through thereview process and tens of thousands of developers participate inthe process, as both code authors and reviewers.Authors and reviewers exchange comments through the codereview system, and a review progresses through snapshots of filesaffected by the change. Each reviewer comment is attached to aspecific line and column range in a specific file snapshot. To resolvea comment, the author typically modifies the file in their local copy

Figure 1: Example comment posted by a human reviewer.and exports a new snapshot for the next round of code review.When the author and all reviewers are satisfied and no automatedanalysis is blocking the merge, the code is merged into the codebase.The most expensive part of the code review process is the timespent by code authors and reviewers “shepherding” a change (frominitial coding, through addressing reviewer comments and ensur-ing all automated analyses pass, to finally merging the changeinto the codebase). While the process is optimized with automatedsystems analyzing the code before the review (notably automaticcode formatting without human intervention), code reviews stillcost thousands of developer-years per year. Thus, even single-digitpercentage savings translate into significant business impact.

2.2 Best PracticesAbest practiceis a specific use of programming language that isconsidered superior, and abest practice documentdescribes howit should be applied and what benefits it brings.Best practice URLrefers to a best practice document or specific section therein, andbest practice violationrefers to a specific piece of code that does notadhere to a best practice, but can be changed to do so. If clear fromcontext, we use the termsURLandviolationto refer to best practiceURL and best practice violation, respectively.Google’s central code repository contains code in many lan-guages, with C++, Java, Python and Go exceeding 100 million lineseach [19readily available to all developers. Many of these languages haveadditional language primers, documentation for core libraries, andtip-of-the-week style newsletters. While these materials are notas strictly enforced as style guides, they are frequently referencedin code reviews. Some languages boast hundreds of pages of suchdocumentation. Both code authors and reviewers are expected toverify that the code follows all best practices.A formal mechanism called “readability”, introduced more thana decade ago, ensures that best practices are followed consistently.Dedicated style experts in a given language, called “readabilitymentors”, guide inexperienced developers towards proficiency inthe language [23best practice in a few sentences and at the end of the commentinclude a URL for the change author as a reference. Figure 1 showsan example of a comment posted by a readability mentor.

AI-Assisted Assessment of Coding Practices in Modern Code Review AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

Figure 2: Architecture of the model-training pipeline.The readability process has some drawbacks. For authors, it in-creases development time due to additional review rounds. For read-ability mentors, it can become a monotonous and time-consumingtask. It requires mastering hundreds of evolving best practices, in-cluding the identification and deprecation of outdated rules, anddocumenting them (with relevant links) in the code-review sys-tem. Additionally, it requires tracking, sometimes through multipleiterations, ensuring that all violations have been remedied.

3 APPROACHIn response to the challenges described sections 2.1 and 2.2, wedeveloped AutoCommenter, a code analysis tool that automaticallydetects best practice violations. It aims to provide timely feedbackfor code authors and to alleviate the need for manual best-practicereviews, thereby allowing reviewers to focus on code functionality.3.1 Model and Task DefinitionAutomating best practice analysis requires a model that can rep-resent source code, pinpoint violation locations, and identify theviolated best practice. We target a text-to-text transformation usinga traditional transformer approach based on T5, using T5X [22The best practice analysis is one task in a multi-task large se-quence model. In addition to the standard pretraining task for T5,span denoising (predicting masked tokens), other tasks used totrain this model include code-review comment resolution, nextedit prediction, variable renaming, and build-error repair [9training corpus consists of over 3 billion examples, of which thebest practice analysis dataset contributes about 800k examples. Themodel was trained using the standard cross-entropy loss, typical forsuch models, and tuned to maximize the sequence accuracy metric,predicting the exact target text for each example.For the best practice analysis, theinputto the model is a taskprompt and source code, and thetargetis a source code loca-tion and a URL for a best practice violation. The task prompt isformatted as a fixed-text code comment, using the programminglanguage’s appropriate commenting style. It describes the task innatural language and precedes the source code, which is a directtextual representation of one file. If the input exceeds the modelcontext window, it is truncated. The location is a byte offset in thesource code, and the URL references the violated best practice. A do-main specific language defines the target format, and a special caseis the “empty” target, if there are no violations. In addition to thetarget, the model outputs a confidence score ranging from 0 to 1.Consider the following input/target example for the Go language.Input

/ / [

∗

/ / P a c k a g e a d d i t i o n p r o v i d e s Add

package

a d d i t i o n

/ / R e t u r n a sum

func

Add ( v a l u e 1 , v a l u e 2

i n t

)

i n t

{

return

v a l u e 1 + v a l u e 2

}

Target

INSERT 1 5 3 COMMENT h t t p s :

/ / go . d e v / d o c / comment # f u n c

The first line of the input is the fixed-text task prompt; the rest isthe source code. The target gives the location (byte offset 153 corre-sponds to the start of theAddfunction) and ago.devURL, pointingto the exact part of the Go language style guide that the functioncomment violates (in this case, the usual practice of starting a com-ment with the function name). Note that the target may contain no,one, or multiple (concatenated) location-URL pairs, depending onthe number of violations in the source code.

3.2 Model TrainingFigure 2 shows the architecture of the model-training pipeline,which consists of three parts. We split dataset creation into twosteps (preprocessing and curation) because the first step is signifi-cantly more expensive as it operates on a much larger amount ofdata. The output of the preprocessing step is agnostic to the model’sinput/target representation. This separation improves feature ve-locity by enabling quick iterations on example representations andother example-level adjustments. The preprocessing step uses afault-tolerant scheduling system and periodically extracts relevantcode comments to ensure that new data is readily available.3.2.1 Large-scale preprocessing.The training examples are createdfrom real code review data, but not all code comments are suitablefor model training. Therefore, the preprocessing step, identifiesrelevant code comments—human authored comments that containa URL pointing to a best practice document. For each comment,the preprocessing step then collects the corresponding source codeand relevant metadata, including the comment’s location in thesource code and its creation time. The output of this step is a setof relevant code comments, each with all the data necessary forcurating examples for model training.

AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

Manushree Vijayvergiya et al.3.2.2 Dataset curation.Dataset curation is a single, on-demandprocessing step, implemented as a Beam1pipeline. It converts eachrelevant code comment, based on the input/target format describedin section 3.1, into the standard TensorFlowExampledata structure.3.2.3 Training and fine-tuning.The curated examples are useddirectly for model training and evaluation. We use the T5X frame-work [221000 steps, and use Tensorboard for monitoring the training.

3.3 Model SelectionTwo intrinsic evaluations on historical data inform our selection ofa model checkpoint, confidence thresholds, and a decoding strategy.First, an evaluation on the validation and test datasets providesestimates of precision and recall on a per-file basis. Second, anevaluation on full historical code reviews provides an estimate ofthe total number of comments per code review, indicating howoften developers would interact with AutoCommenter.3.3.1 Evaluation on Validation and Test Datasets.We temporallysplit the dataset to ensure that the model has not been trained onfuture code-review snapshots of the code comments in the valida-tion and test datasets. In our dataset, 85% of files have exactly onerelevant code comment, 11% have two, and 4% have three or more.We define a prediction to becorrectif the predicted code location(s)and URL(s) match the expected values, regardless of order.Recall that the model provides a confidence score for each pre-diction, which introduces another parameter: a prediction can besuppressed if its confidence score is below some threshold𝑡. Wedefine𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛

𝑡as the number of correct predictions whose confi-dence score is greater than𝑡divided by the number of all predictionswhose confidence score is greater than𝑡; we define𝑅𝑒𝑐𝑎𝑙𝑙

𝑡analo-gously. These definitions allow us to estimate how many (in)correctresults would be shown to a user, as a function of𝑡.𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛

𝑡and𝑅𝑒𝑐𝑎𝑙𝑙

𝑡are used for model checkpoint comparisons during training.While this evaluation avoids data leakage and allow us to auto-matically evaluate model performance, it has a limitation: whileit is reasonable to assume that the human comments for a givencode-review snapshot are correct, they are not exhaustive. In otherwords, it is possible that the code in a given code-review snapshotcould be improved according to multiple best practices, but a hu-man reviewer did not post comments (with URLs) for all of them.This can happen for several reasons:

•Missing references: A reviewer may comment on an issue,but did not include a URL as a reference.

•Selective commenting: A reviewer may comment on an issueonce, expecting the author to apply a fix throughout.

•Varied expertise or focus: A reviewer may not be familiar withall best practices, or simply choose not to comment on anissue in the context of a given code review (e.g., focusingonly on changed code).While most files in our dataset have only one relevant comment,anecdotal evidence based on manually inspecting “incorrect” pre-dictions suggests that multiple best-practice comments are typicallypossible due to the reasons stated above. Given that our ground-truth data is incomplete, our precision and recall measures are noisy.

1

https://beam.apache.org/Therefore, we employ a complementary evaluation, described next,to increase confidence in overall model performance.3.3.2 Evaluation on Full Historical Code Reviews.To accuratelygauge potential comment volume in a live setting, we evaluateAutoCommenter on a set of historical code reviews, using a specificmodel checkpoint and threshold. The predicted comments are notretroactively posted in the code review system, but rather loggedin a database for analysis. This allows us to estimate the expectedposting frequency—both at per-file and per-code-review granularity.Because developers interact with AutoCommenter for an entireset of code changes subject to code review, this evaluation is animportant step before production deployment. As an added benefit,this step allows for further optimizations and assessment of postingfrequencies for different user groups, programming languages, etc.3.4 Inference InfrastructureThe core of AutoCommenter is a central best practice analysis ser-vice. This service takes as input one or more source files for analysis.For each file, it constructs a model input (section 3.1), encodes itin the standard TensorFlowExampledata structure, and queriesthe model. The model itself is served by a model service that usesTensorFlow’sExampledata structure as a domain agnostic input-output format. Finally, the best practice analysis service performsa series of filtering steps (section 4), which suppress low-qualitypredictions, and returns the remaining predictions.

3.5 IDE and Code Review IntegrationDevelopers interact with AutoCommenter’s analysis service intwo ways—directly through an IDE plugin, or indirectly throughthe code review system. The code review system is used by alldevelopers at Google, and the IDE by almost all of them.AutoCommenter’s comments appear in the IDE as diagnosticsmarked with a blue curly underline, spanning the relevant code snip-pet. Hovering over the underlined code reveals the full commentwith a concise summary of the best practice, including a clickablelink to the relevant best practice document. This embedded infor-mation streamlines the workflow for developers by eliminating theneed to switch between the IDE and a web browser for unfamiliarbest practices. Since comments in the IDE need to be generated inreal-time, we aim to generate comments with sub-second latency.In the code review system, AutoCommenter runs after eachupdate (i.e., on each new code-review snapshot), automaticallyposting comments if it detects any violations. Comments producedby automated tools are visually similar to comments produced byhumans, but have a differently colored background.Figure 3 shows an example comment generated and posted byAutoCommenter in the code review system. Note the thumbs upand thumbs down buttons (right), which authors and reviewers canclick if they find a comment particularly useful or not. Also notethe “Please fix” button (left), which is visible to reviewers. If clicked,a new comment is generated indicating that the reviewer believesthe comment is significant and must be addressed before the codeis merged into the codebase. These feedback buttons are standardin the code review system, present on all comments generated byautomated tools (e.g., [7,13acceptance. The IDE provides a similar feedback mechanism.

AI-Assisted Assessment of Coding Practices in Modern Code Review AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

Figure 3: Example comment posted by AutoCommenter.

4 DEPLOYMENTWe deployed AutoCommenter to all developers at Google over aperiod of time between July 2022 and October 2023:

•

until Jul. 2022—teamfooding

: this paper’s authors.

•

Jul. 2022—early adopters

: around 3 thousand volunteers.

•

Jul. 2023—A/B experiment

: about half of all developers.

•

since Oct. 2023—general availability

: all developers.Note that due to industrial confidentiality reasons we are unableto disclose absolute numbers of code reviews, developers, files,comments, or distribution of duration of code reviews. We reporton relative measures, where appropriate, and relevant trends.We continuously evaluated and improved the performance ofAutoCommenter, using an iterative refinement approach:

•Evaluation on historical data (section 3.3) to get directionalinsight into how well the model does at the task and to definethresholds and select a decoding strategy.

•Monitoring and analysis of user interaction and direct feed-back through feedback buttons and issue reports.

•Targeted human evaluation based on patterns observed dur-ing other evaluation steps.Figure 4 shows the ratio of positive to negative developer feed-back on posted code review comments and IDE diagnostics overtime. The dashed line shows the total count of feedback clicks de-velopers provided per month. As is expected, this count is muchlower during the early-adopter stage. Additionally, the volatility ishigher in this stage because we actively refined AutoCommenter.Recall the three feedback buttons within the code review system(figure 3), which allow developers to express positive and negativesentiment about a posted comment. We consider comments with athumbs up or “Please fix” as positive, and comments with a thumbsdown as negative; we define theuseful ratioas the ratio of positivecomments to all comments with feedback.The remainder of this section describes specific observationsand corresponding refinements that we made during deployment.

4.1 Selecting Threshold and Decoding Strategy4.1.1 Threshold.During initial deployment we wanted to carefullymanage the trust developers had in AutoCommenter and startedwith a high confidence threshold of𝑡

=0.98. We manually sampled

Figure 4: Developer feedback throughout deployment.several hundred results and observed that around 80% of predictionsbelow the threshold were still correct—that is, the false-negativerate was very high at𝑡

=0.98. Additionally, we observed thatpredictions in Python showed a significantly different distributionof confidence scores, which were disproportionately impacted bythresholding. We conjecture that the training dataset composition(number of distinct URLs and URL frequencies) and specificity of thebest practice documents are reasons, but leave a deeper investiga-tion to future work. An attempt to deploy per-language thresholdsproved ineffective as a single threshold per language still did notadequately capture the model’s ability to correctly predict hundredsof diverse best practices. This led to a lack of diversity in predictedURLs as the model tended to produce higher scores for some URLsvs. others, irrespective of correctness. These observations led to thefirst major change to AutoCommenter: per-URL thresholds com-puted based on the intrinsic evaluation on the validation dataset.4.1.2 Decoding.An evaluation using per-URL thresholds withgreedy decoding on full historical code reviews revealed that Auto-Commenter detects violations in 6% of all changed files. However,80% of comments would have been posted on lines of code notmodified by the author. Developers typically do not take action onunchanged code. Consequently, AutoCommenter filters generatedcomments on unchanged lines of code, reducing the ratio of com-ments in changed files to 1.3%. In order to increase this ratio, weexperimented with different decoding strategies: greedy (default),beam search, top-k, and top-p sampling. We settled on beam search(generating𝑛

=4potential responses), which tripled the postingfrequency to 3.9%. It also yielded a substantially higher URL diver-sity: the 10 most-frequently posted URLs accounted for 41% of allcomments, compared to 80% for greedy search.Latency is another important aspect when choosing a decodingstrategy for deployment. While beam search increased the postingfrequency and diversity, inference became noticeably slower (me-dian latency of 2 seconds). Given that this latency is prohibitivefor interactive use in the IDE, we ultimately decided to use beamsearch for the code review system and greedy search for the IDE.

AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

Manushree Vijayvergiya et al.

4.2 Suppressing Outdated Best PracticesAfter launching AutoCommenter to around 3 thousand voluntaryfirst-adopters, we noticed a large number of issues being filed byusers within a few days. Many of these corresponded to a singleURL2, which describes best practices related to Python imports.However, the canonical source for some type names had changedin Python 3.9, and the best practice had also changed in early 2022.Since our training data stretches before 2022, it contained a num-ber of best practice comments that were no longer applicable. Werealized that this is a recurring pattern: as languages evolve, ornew libraries are introduced, best practices evolve as well. Oneway of mitigating the problem is to filter out such data (whenevera rule changes), and retrain the model. This is however time andresource-consuming: it requires full data regeneration, model train-ing, evaluation, and rollout. In the meantime, the “outdated” modelneeds to be either switched off, causing downtime of the system, oraffected predictions need to be suppressed. Otherwise, the systemcould quickly lose developer trust. We opted for suppression of spe-cific best-practice predictions, using conditional filtering (matchingregular expressions on the source code) for two reasons. First, itcan be dynamically deployed and immediately applied. Second, itallows for granular filtering of predictions.

4.3 Independent Rating of Selected CommentsAfter several months of early usage, we observed that the usefulratio plateaued at around 54%. To understand the reasons, iden-tify areas for improvement, and prepare for a wider deployment,we conducted an independent human rating study in April 2023,analyzing a sample of around 370 posted comments that receiveddeveloper feedback during our first-adopters deployment.To gather diverse perspectives on the usefulness of comments werecruited 15 raters—developers from partner teams. We asked themto rate AutoCommenter’s comments that received explicit userfeedback. We did not show the original user feedback to the rater, toavoid biasing their evaluation. The raters assessed each comment’susefulness based on the linked best practice and the surroundingcode. We instructed them to focus on comment correctness, but alsowhether the comment would be actionable to them as an author(e.g., would they resolve a comment that is technically correct butdoes not seem worth resolving in a specific instance). They wereencouraged to provide free-form feedback on each comment.The useful ratio from the rater evaluation was 60%, slightlyhigher than the 54% from the developer feedback on the samecomments, but well below our target of 80% for wider deployment.The most interesting finding from this study was that there wereclear patterns of not useful comments. Here are some examples:Several topics or complex topic:For example, one URL pointsto a section that describes multiple guidelines for interacting withthe Python linter, including cases where it often triggers and waysto suppress it. An author may struggle to understand what specificguideline a posted comment is referring to and how to resolve it.Similarly, the guidance on writing good function documentation inC++ is a full page of dense text. Raters frequently noted a disconnectbetween a best practice (and AutoCommenter’s concise summary)and the actual code, even when it contained a relevant violation.

2

https://github.com/google/styleguide/blob/gh-pages/pyguide.md#22-importsImportance of high-quality summaries:Raters often foundthat AutoCommenter’s summary, which was generated by scrapingthe document source and sometimes missing, failed to adequatelyexplain the relevance of the cited guideline to the comment/code.Subjective and potentially contentious topic:One exampleis avoiding flags in library code. Flags can cause problems whenused in libraries, but some libraries are specifically designed tohave many features configurable via flags. Additionally, legacy codemay not adhere to this guideline and reviewers will not enforce it.The model did not learn these nuances and sometimes predicted aviolation when an author added a new flag to an existing library.Systematic model error for some guidelines:One interestingexample is a guideline that promotes the use of the member functionpush_backoveremplace_backfor C++ vectors when both functionscan be used with the same arguments to achieve the same effect.The model had learned to predict this, but it would also predictit in cases whereemplace_backis warranted, and also when anunrelated type had a member function called

push_back

.Correct but low-value comments:A missing period at theend of a sentence in a code comment is often allowed by humanreviewers. While technically correct, asking the author to go backto their IDE and fix the issue may provide net negative value.The insights from the rater study informed two changes to Auto-Commenter. First, the rater study identified 17 non-actionable URLs,whose suppression increased the historical useful ratio from 54% to66% on developer feedback, and from 60% to 74% on rater feedback.We further analyzed comments linked to similar, unrated URLsand suppressed an additional 5. Second, we reviewed and manuallyupdated summaries for all frequently posted URLs. Together, thesechanges were sufficient to reach our target useful ratio of 80% forthe next stage of deployment.

4.4 A/B ExperimentIn July 2023, we deployed AutoCommenter to about half of all devel-opers in the context of an A/B experiment. We randomly assigneddevelopers to a an experiment group (AutoCommenter enabled)and a control group (AutoCommenter disabled). We randomizedbased on the last few digits of the SHA256 hash of the developersemail address, and we verified that both groups did not differ insize and composition, including distribution of tenure, seniority,programming languages and business units. We also confirmed thatnone of the variables measured during the experiment differed be-tween the control and the experiment group before the experimentbegan. The comment posting frequency during the experiment wasin line with expectations (section 4.1).We did not detect any statistically significant change in anyof the following: total duration of code reviews, time developersactively spent on the code review, the number of comment-responseiterations between the author and the reviewer. We did, however,detect a slight improvement in coding speed. We conjecture thatthe reduction in context switches to documentation leads to thispositive effect. We leave a deeper investigation for future work.Based on the results, we concluded that there are no adverse effects,and deployed AutoCommenter to all developers in October 2023.

AI-Assisted Assessment of Coding Practices in Modern Code Review AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

Figure 5: Cumulative distribution of comments per URL forthe automated comments generated by AutoCommenter inproduction and human comments in the training data.

5 EVALUATIONBased on the useful ratio and user feedback gathered since March2023, we conclude that developers are generally satisfied with thecomments produced by AutoCommenter. We continuously refineour dataset preparation, thresholds, URL suppression and summa-rization by analyzing user feedback, to ensure that AutoCommenterdelivers high positive impact on the developer workflow.Beyond developer satisfaction, with several months in wide re-lease to all of Google, we evaluated three additional aspects ofAutoCommenter’s performance:

(1)Comment resolution:How often do developers modifytheir code to resolve AutoCommenter’s posted comments?

(2)AutoCommenter vs. human comments:How well do Au-toCommenter’s comments cover the best practice documentsthat human reviewers reference in their comments?

(3)AutoCommenter vs. linters:To what extent does Auto-Commenter’s output go beyond the capabilities of traditionalstatic analysis tools?

5.1 Comment ResolutionDevelopers rarely giveexplicit feedbackon AutoCommenter’s com-ments by clicking the thumbs up/thumbs down buttons in the codereview system and IDE, and the “Please fix” button in the codereview system (figure 3): about 10% of automated comments in thecode review system and 2% of diagnostics in the IDE received ex-plicit feedback, which is comparable to other automated analyses atGoogle. At the same time, developers hover over approximately 50%of the AutoCommenter’s IDE diagnostics, and prior work showedthat developers often resolve automated comments without explicitfeedback [18menter’s comments, we conducted an offline analysis, estimatingthe ratio of comments resolved by subsequent code changes.To analyze comment resolution, we extracted historical changesfocused on files with automated comments from AutoCommenter.For each, we extracted the initial snapshot where the comment wasposted and the snapshot that the developer eventually merged intothe codebase. Each comment spans a specific range of lines. Weused an automated AST-based line mapping approach [18these snapshots, to identify comments that the model originally

Figure 6: The top-50 most frequently predicted URLs catego-rized into types. Linter indicates whether a linter that detectsa violation exists or can easily be built.predicted on the first snapshot, but did not predict on the mergedsnapshot. Such pairs of snapshots indicated that a comment mayhave been resolved, but it is possible that unrelated code changescould have led to a specific comment no longer being predicted.An automated analysis of 6000 snapshot pairs revealed that in50% of cases the comment was absent from the submitted snapshoton the lines it was originally posted. We manually inspected arandom sample of 40 such pairs. We found that in 80% of cases, achange made by the author directly resolved the issue describedby the posted comment. Therefore, we estimate that the comment-resolution rate is about 40%, which is significantly larger than theratio of comments with explicit positive feedback to all comments.5.2 AutoCommenter vs. Human CommentsFigure 5 compares the cumulative distribution of comments (perunique URL to a best practice document) for the automated com-ments generated by AutoCommenter in production and humancomments in the training data. The x-axis is the rank of the URLwhen all URLs ever used in automated comments are sorted byfrequency. For example, the most frequently used URL has rank 1,and it accounts for 9.9% of all automated comments. This same URLappeared in 4.3% of the human created comments in the trainingdata. In total, AutoCommenter has created comments for 330 dis-tinct URLs. The set of URLs used by AutoCommenter covers 68%of historical human comments with a best practice URL. This is agood result: it demonstrates that AutoCommenter is not focusingon obscure best practices that are rarely referenced by reviewers.On the other hand, despite utilizing beam search, URL diversityremains relatively low. The top-85 URLs make up 90% of commentscreated by AutoCommenter. The same set of URLs cover 35% ofhuman comments with best practice URLs. Improving URL diver-sity and coverage of best practices in automated comments whilemaintaining accuracy and low latency is one of our top priorities.

5.3 AutoCommenter vs. LintersTo understand to what extent AutoCommenter provides value be-yond linters that can efficiently and precisely check some of thebest practices, we sampled the top-50 most frequently predictedviolations—that is, the top-50 URLs in figure 5. For each sampled

AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

Manushree Vijayvergiya et al.URL, we inspected its best practice document and determined (1) thebest-practice type (section 1) and (2) whether a linter that detects acorresponding violation exists or can be easily built. Specifically,three authors, each with over 10 years of experience in buildingstatic analysis tools, read the documentation and independentlycategorized the URLs. There were no disagreements on the best-practice type, but there were disagreements on whether a lintercan be easily built for about 15% of URLs. The three authors re-solved these disagreements through majority vote and discussion.Disagreements stemmed from ambiguous best practices, and thosewith multiple guidelines. For example, while checking the pres-ence of code documentation is relatively straightforward, reasoningabout justified exceptions and clarity of content may not.Figure 6 shows the distribution of the 50 sampled URLs, brokendown by type and whether violations can be detected by a linter.For 33/50 (66%) of these best practices, violation detection is beyondthe scope of traditional static analysis.

6 LESSONS LEARNEDBased on our experience developing and deploying AutoCommenter,we summarize a few key lessons learned:

•Complementing traditional analyses: AutoCommenter’sLLM-backed approach generates comments for 68% of bestpractices frequently referenced by human reviewers. Manyof these are out of scope for traditional static analyses.

•Intrinsic evaluation vs. real-world performance: Intrin-sic evaluations and real-world performance can diverge sig-nificantly: our intrinsic evaluation, using a dataset of real-world human comments together with a state of the artmodel architecture and training process, indicated a promis-ing model, but our extrinsic evaluations and system improve-ments proved essential for a successful deployment.

•Monitoring user acceptance is critical: Even a few nega-tive user experiences can erode trust in an automated system.Continuously monitoring and analyzing real-world feedbackwas crucial in detecting such instances and identifying reme-dies. In the case of AutoCommenter, a simple suppressionmechanism was sufficient to strongly improve user accep-tance to over 80% without major sacrifices in efficacy.

7 RELATED WORKJohnson [15those 50 years, a considerable body of research on automated staticanalysis was produced: a recent literature review by Heckman andWilliams [10developers interact with static analysis. Johnson et al. [14explorechallenges developers face when trying to use static analysis. Theresults of their study highlights the importance of good integrationinto existing developer workflows and the importance of develop-ing and maintaining trust in the tool. Vassallo et al. [27explorehow developers interact with static analysis in different contexts,including coding and code review. They too find that integrationinto existing workflows plays a major role in developers willing-ness to use the tools and that high quality of results is extremelyimportant. Beller et al. [6studied usage of static code analysis in alarge number of open source projects. Among other findings, theyhighlight that how automated analysis is and should be used variesbased on the programming language.In contrast, using machine learning for code analysis is a compar-atively new and less understood field. A number of recent publica-tions (e.g., Hong et al. [11, Li et al. [16, Li et al. [17, Thongtanunamet al. [24, Tufano et al. [25, and Tufano et al. [26) report on modelevaluations and propose tools for automated code review. Whilethese models and the review comment generation task are very sim-ilar to the model presented in this paper, evaluations largely focusedon historical datasets. As discussed in section 3.3.1 an intrinsic eval-uation on only historical comments is somewhat limited and cansometimes fail to predict real-world performance. Another recentpublication by Frömmgen et al. [9presents an evaluation of a livesystem, but for the opposite task: creating code from commentsrather than comments from code.

8 CONCLUSIONVerifying that code adheres to best practices is a common task inmodern code review processes. While some best practices can beautomatically verified with traditional tools such as linters, manyrequire the knowledge and judgement of experienced developers,which requires time and effort.This paper reports on our experience developing, deploying, andevaluating AutoCommenter, an LLM-backed code review assistantsystem. Specifically, it lays out the entire process from task andmodel design, over intrinsic evaluations and system calibrations,to a staged roll out and end-user evaluation.The evaluation results show that it is feasible to develop anend-to-end system with capabilities well beyond traditional toolswhile achieving a high degree of end-user acceptance. These resultsare a promising first step towards the deployment of sophisticatedcode-review assistants and automated code reviews.Our priority was to ensure a positive developer experience bydesigning AutoCommenter to have very high precision. While recallwas not the primary focus, we recognize its significance and planto explore what changes in the model and system architecture canimprove recall. For example, the model we used in 2022 was state ofthe art at the time. However, it has a limited context window of 2048tokens which suffices for only around 200 lines of code. Currentstate of the art models have context windows of tens of thousands oftokens during training and over a million tokens during inference.This leap opens up opportunities for new features and significantimprovement in existing ones.

9 ACKNOWLEDGEMENTSThis work is the result of years of collaboration between teams inGoogle Core Systems and Google DeepMind. We are grateful for thesupport and advice of all our team members and leadership, includ-ing Alberto Elizondo, Alexander Frömmgen, Ballie Sandhu, ChanduThekkath, Chris Gorgolewski, David Tattersall, Ilya Cherny, JacobAustin, Katja Grünwedel, Kristóf Molnár, Lera Kharatyan, Luka Ri-manić, Madhura Dudhgaonkar, Marc Brockschmidt, Marcus Revaj,Maxim Tabachnyk, Nina Chen, Niranjan Tulpule, Nitya Ramani,Paige Bailey, Pavel Sychev, Pierre-Antoine Manzagol, Quinn Madi-son, Roger Fleig, Satish Chandra, Savinee Dancs, Stoyan Nikolov,Subhodeep Moitra, and Vaibhav Tulsyan.

AI-Assisted Assessment of Coding Practices in Modern Code Review AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

REFERENCES

2024. Google Style Guides. https://google.github.io/styleguide/. Accessed:2024-03-15.

2024. Linux kernel coding style. https://www.kernel.org/doc/html/v4.10/process/coding-style.html. Accessed: 2024-03-15.

2024. PEP 8 – Style Guide for Python Code. https://peps.python.org/pep-0008/.Accessed: 2024-03-15.

2024. Rust Style Guide. https://doc.rust-lang.org/nightly/style-guide/. Accessed:2024-03-15.

Alberto Bacchelli and Christian Bird. 2013. Expectations, outcomes, and chal-lenges of modern code review. In2013 35th International Conference on SoftwareEngineering (ICSE)

. 712–721. https://doi.org/10.1109/ICSE.2013.6606617

Moritz Beller, Radjino Bholanath, Shane McIntosh, and Andy Zaidman. 2016.Analyzing the state of static analysis: A large-scale evaluation in open source soft-ware. In2016 IEEE 23rd International Conference on Software Analysis, Evolution,and Reengineering (SANER)

, Vol. 1. IEEE, 470–481.

Zimin Chen, Małgorzata Salawa, Manushree Vijayvergiya, Goran Petrović, MarkoIvanković, and René Just. 2023. MuRS: Mutant Ranking and Suppression usingIdentifier Templates. InProceedings of the Symposium on the Foundations ofSoftware Engineering (FSE)

. 1798–1808.

M. E. Fagan. 1976. Design and code inspections to reduce errors in programdevelopment.IBM Systems Journal15, 3 (1976), 182–211. https://doi.org/10.1147/sj.153.0182

Alexander Frömmgen, Jacob Austin, Peter Choy, Nimesh Ghelani, Lera Kharatyan,Gabriela Surita, Elena Khrapko, Pascal Lamblin, Pierre-Antoine Manzagol, MarcusRevaj, Maxim Tabachnyk, Daniel Tarlow, Kevin Villela, Daniel Zheng, SatishChandra, and Petros Maniatis. 2024. Resolving Code Review Comments withMachine Learning. InInternational Conference on Software Engineering: SoftwareEngineering in Practice (ICSE-SEIP)

.

Sarah Heckman and Laurie Williams. 2011. A systematic literature review ofactionable alert identification techniques for automated static code analysis.Information and Software Technology53, 4 (2011), 363–387. https://doi.org/10.1016/j.infsof.2010.12.007 Special section: Software Engineering track of the 24thAnnual Symposium on Applied Computing.

Yang Hong, Chakkrit Tantithamthavorn, Patanamon Thongtanunam, and AldeidaAleti. 2022. Commentfinder: a simpler, faster, more accurate code review com-ments recommendation. InProceedings of the Joint Meeting of the European Soft-ware Engineering Conference and the Symposium on the Foundations of SoftwareEngineering (ESEC/FSE)

. 507–519.

Marko Ivanković, Goran Petrović, René Just, and Gordon Fraser. 2019. CodeCoverage at Google. InProceedings of the Joint Meeting of the European Soft-ware Engineering Conference and the Symposium on the Foundations of SoftwareEngineering (ESEC/FSE)

. 955–963.

Marko Ivanković, Goran Petrović, Yana Kulizhskaya, Mateusz Lewko, Luka Kali-novčić, René Just, and Gordon Fraser. 2024. Productive Coverage: Improvingthe Actionability of Code Coverage. InInternational Conference on SoftwareEngineering: Software Engineering in Practice (ICSE-SEIP)

.

Brittany Johnson, Yoonki Song, Emerson Murphy-Hill, and Robert Bowdidge.2013. Why don’t software developers use static analysis tools to find bugs?. In2013 35th International Conference on Software Engineering (ICSE). IEEE, 672–681.Stephen C Johnson. 1977.Lint, a C program checker. Bell Telephone LaboratoriesMurray Hill.

Lingwei Li, Li Yang, Huaxi Jiang, Jun Yan, Tiejian Luo, Zihan Hua, Geng Liang,and Chun Zuo. 2022. Auger: Automatically generating review comments withpre-training models. InProceedings of the Joint Meeting of the European Soft-ware Engineering Conference and the Symposium on the Foundations of SoftwareEngineering (ESEC/FSE)

. 1009–1021.

Zhiyu Li, Shuai Lu, Daya Guo, Nan Duan, Shailesh Jannu, Grant Jenks, DeepMajumder, Jared Green, Alexey Svyatkovskiy, Shengyu Fu, and Neel Sundaresan.2022. Automating code review activities by large-scale pre-training. InProceedingsof the 30th ACM Joint European Software Engineering Conference and Symposiumon the Foundations of Software Engineering(<conf-loc>, <city>Singapore</city>,<country>Singapore</country>, </conf-loc>)(ESEC/FSE 2022). Association forComputing Machinery, New York, NY, USA, 1035–1047. https://doi.org/10.1145/3540250.3549081

Goran Petrović, Marko Ivanković, Gordon Fraser, and René Just. 2023. Please fixthis mutant: How do developers resolve mutants surfaced during code review?. InInternational Conference on Software Engineering: Software Engineering in Practice(ICSE-SEIP)

. 150–161.

Rachel Potvin and Josh Levenberg. 2016. Why Google Stores Billions of Linesof Code in a Single Repository.Communications of the ACM (CACM)59 (2016),78–87. http://dl.acm.org/citation.cfm?id=2854146

Peter Rigby, Brendan Cleary, Frederic Painchaud, Margaret-Anne Storey, andDaniel German. 2012. Contemporary Peer Review in Action: Lessons from OpenSource Development.IEEE Software29, 6 (2012), 56–61. https://doi.org/10.1109/MS.2012.24

Peter C. Rigby and Christian Bird. 2013. Convergent contemporary software peerreview practices. InProceedings of the 2013 9th Joint Meeting on Foundations ofSoftware Engineering(Saint Petersburg, Russia)(ESEC/FSE 2013). Association forComputing Machinery, New York, NY, USA, 202–212. https://doi.org/10.1145/2491411.2491444

Adam Roberts, Hyung Won Chung, Gaurav Mishra, Anselm Levskaya, JamesBradbury, Daniel Andor, Sharan Narang, Brian Lester, Colin Gaffney, AfrozMohiuddin, et al.2023. Scaling up models and data with t5x and seqio.Journalof Machine Learning Research

24, 377 (2023), 1–8.

Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, and AlbertoBacchelli. 2018. Modern Code Review: A Case Study at Google. InInternationalConference on Software Engineering: Software Engineering in Practice (ICSE-SEIP).181–190.

Patanamon Thongtanunam, Chanathip Pornprasit, and Chakkrit Tantithamtha-vorn. 2022. Autotransform: Automated code transformation to support moderncode review process. InProceedings of the International Conference on SoftwareEngineering (ICSE)

. 237–248.

Rosalia Tufano, Ozren Dabić, Antonio Mastropaolo, Matteo Ciniselli, and GabrieleBavota. 2024. Code Review Automation: Strengths and Weaknesses of the Stateof the Art.

IEEE Transactions on Software Engineering (TSE)

(2024).

Rosalia Tufano, Simone Masiero, Antonio Mastropaolo, Luca Pascarella, DenysPoshyvanyk, and Gabriele Bavota. 2022. Using pre-trained models to boost codereview automation. InProceedings of the International Conference on SoftwareEngineering (ICSE)

. 2291–2302.

Carmine Vassallo, Sebastiano Panichella, Fabio Palomba, Sebastian Proksch, Har-ald C Gall, and Andy Zaidman. 2020. How developers engage with static analysistools in different contexts.Empirical Software Engineering25 (2020), 1419–1457.T. Winters, T. Manshreck, and H. Wright. 2020.Software Engineering at Google:Lessons Learned from Programming Over Time. O’Reilly Media. https://books.google.ch/books?id=TyIrywEACAAJ

Received 2024-04-05; accepted 2024-05-04

Training and fine-tuning (on demand)

Worker

Worker

Workers

Source

repository

Comment

storage

Scheduler

Relevant

code

comments

Worker

Worker

Workers

Examples

(temporal

splits)

Worker

Worker

TPU pods

Tensorboard

Model

checkpoints

Input/target

format

Large-scale preprocessing (periodic)

Dataset curation (on demand)

Code idioms

Documentation

Formatting

Language

Naming

0

5

10

Number of distinct URLs

Linter

Yes No/Partially
