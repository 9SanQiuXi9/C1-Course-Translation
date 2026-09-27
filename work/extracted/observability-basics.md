---
source_file: "data/materials/CS146S_offline/pages/observability-basics.html"
origin_url: "https://last9.io/blog/traces-spans-observability-basics/"
title: "Understanding Traces and Spans: Core Concepts"
extract_method: "html"
extract_warnings:
  - "AGGRESSIVE_STRIP_REVERTED：按关键词剥离 5 个区块后正文下降 94.0%（>40%），已全部加回，避免剥掉正文。该页结构特殊，建议人工抽查。"
src_sha256: "4986d7fe57f73831fc7781fc48fb67175ed50fac8b0da8e55c855f8df3704ea8"
chars: 14972
code_blocks: 2
tables: 1
links: 45
garbage_rate: 0.0962
heading_levels_seen:
  h1: 1
  h2: 10
  h3: 17
  h4: 2
---

![Cookie](/_astro/cookie-illustration.4Ddzj9Hm_ZT4qFS.svg)

We use cookies to customize your Last9 experience.
 What's your preference?

Essential only

Accept all

[Last9](/)

[Book demo
 Open menu](/schedule-demo/)

[Last9](/)

[Book demo
 Close menu](/schedule-demo/)

Product

[Discover](/discover/)

Explore

[Logs](/logs/)

[Traces](/traces/)

[Metrics](/metrics/)

[Control Plane](/control-plane/)

[AI](/mcp/)

[RUM](/docs/discover-applications/)

[Alerting](/alerting/)

Resources

[Guides](/guides/)

[Blog](/blog/)

[Events](/events/)

[Changelog](/changelog/)

More

[Customers](/customers/)

[Docs](/docs/)

[Pricing](/pricing/)

[Last9](/)

Apr 23rd, 2025

## Traces & Spans: Observability Basics You Should Know

Learn how traces and spans help you see inside distributed systems—so you can troubleshoot faster and build more reliable software.

![Anjali Udasi](https://last9.ghost.io/content/images/2024/08/profile_pic.jpeg)

[Anjali Udasi](/blog/authors/anjali/)

![Traces & Spans: Observability Basics You Should Know](https://last9.ghost.io/content/images/2025/04/traces.webp)

#### Contents

https://discord.com/invite/Q3p2EEucx9/

https://www.linkedin.com/company/last9/

https://youtube.com/@last9/

https://x.com/last9io/

In modern software architecture, applications aren't just getting bigger—they're getting more distributed. With microservices, serverless functions, and containers running across multiple environments, understanding what's happening inside your systems can feel like trying to track a single raindrop in a storm.

That's where traces and spans come in. These observability tools aren't just buzzwords—they're your secret weapon for making sense of complex distributed systems. Let's break down what traces and spans are, why they matter, and how you can use them to troubleshoot faster and build more reliable systems.

# Understanding Traces and Spans: Core Concepts

Traces capture the journey of a request as it moves through your distributed system. Think of a trace as the complete story of a request from start to finish—from when a user clicks a button until they see the result.

Spans are the building blocks of traces. Each span represents a unit of work within that journey—like a database query, an API call, or a function execution. Spans nest within each other to show parent-child relationships between operations.

Here's the relationship in simple terms:

- A trace contains multiple spans
- Each span represents one operation
- Spans have timing data and metadata
- Spans can be nested to show how operations relate to each other

<!-- CODE_BLOCK_START id=c1 lang= -->
```
Trace
├── Span (API Gateway)
│   ├── Span (Auth Service)
│   └── Span (User Service)
│       └── Span (Database Query)
└── Span (Response Formatting)
```
<!-- CODE_BLOCK_END id=c1 -->

💡

If you're curious how traces and spans fit alongside

[metrics, logs, and events, this post breaks down all four.](https://last9.io/blog/understanding-metrics-events-logs-traces-key-pillars-of-observability/)

## Benefits of Traces and Spans for DevOps Professionals

You're running a complex system with dozens of microservices. Suddenly, users report the checkout process is slow. Without tracing, you'd need to check each service individually, wasting precious time.

With traces and spans, you can:

1. Find bottlenecks instantly: See exactly which service or function is taking too long
2. Debug across service boundaries: Follow requests as they jump between services
3. Understand dependencies: Visualize how your services connect and depend on each other
4. Improve performance: Identify and fix slow operations with precision
5. Reduce mean time to recovery (MTTR): Get to the root cause faster when issues arise

## Technical Implementation of Traces and Spans

Let's get into the nuts and bolts of how tracing works in distributed systems.

### Trace Context and Propagation

For tracing to work across service boundaries, each service needs to know it's handling part of the same request. This happens through context propagation—passing a trace ID and span ID between services.

When a request first hits your system, it gets assigned a unique trace ID. As the request moves between services, this ID travels with it (usually as HTTP headers). Each service then creates its own spans but links them to the same trace.

### Span Attributes and Events

Spans aren't just timestamps—they're rich with data:

- Name: What operation this span represents
- Timing: Start and end times
- Status: Success, error, etc.
- Attributes: Custom key-value pairs (like user_id or cart_size)
- Events: Notable occurrences within the span
- Links: Connections to other spans

### Sampling Strategies

Tracing everything can create massive amounts of data. That's why most systems use sampling—collecting only a percentage of traces. Smart sampling strategies include:

- Head-based sampling: Decide whether to sample at the beginning of a request
- Tail-based sampling: Decide after the request completes (better for catching errors)
- Priority sampling: Always trace important operations, but sample routine ones

💡

If you're looking to understand the differences between observability, telemetry, and monitoring, check out this helpful post:

[Observability vs Telemetry vs Monitoring.](https://last9.io/blog/observability-vs-telemetry-vs-monitoring/)

## Tracing Implementation Guide: Tools and Frameworks

Ready to add tracing to your systems? Here's what you need:

### OpenTelemetry: The Industry Standard

[OpenTelemetry has become the go-to framework for implementing traces and spans. It provides:](https://opentelemetry.io/)

- Libraries for all major programming languages
- A vendor-neutral API and SDK
- Automatic instrumentation for popular frameworks
- A consistent way to collect and export data

### The Tracing Toolbox

Several tools can help you collect, store, and visualize your traces:

| Tool | Type | Best For |
| --- | --- | --- |
| Last9 | All-in-one observability | Cost-effective, high-cardinality observability with predictable pricing |
| Jaeger | Open-source tracing | Self-hosted tracing visualization |
| Zipkin | Open-source tracing | Simple distributed tracing |
| Grafana Tempo | Tracing backend | Integration with Grafana dashboards |
| OpenTelemetry Collector | Data collection pipeline | Processing and routing telemetry data |

If you're after an observability solution that fits your budget,

[Last9 is worth checking out. With pricing based on ingested events, it keeps things predictable. Plus, our platform handles high-cardinality data at scale and integrates with OpenTelemetry and Prometheus to bring your metrics, logs, and traces together in one place.](https://last9.io/)

### Implementing Tracing in Your Code

Here's a simplified example of how to create spans in a Node.js application using OpenTelemetry:

<!-- CODE_BLOCK_START id=c2 lang= -->
```
// Initialize the OpenTelemetry SDK (once in your app)
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const provider = new NodeTracerProvider();
const exporter = new OTLPTraceExporter({
  url: 'http://localhost:4318/v1/traces',
});
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

// Get a tracer
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('my-service');

// Create spans in your code
async function processOrder(orderId) {
  const span = tracer.startSpan('process-order');

  // Add attributes to the span
  span.setAttribute('order.id', orderId);
  span.setAttribute('customer.type', 'premium');

  try {
    // Do work...

    // Create a child span
    const dbSpan = tracer.startSpan('database-query', {
      parent: span,
    });

    try {
      // Run database query...
      dbSpan.end();
    } catch (error) {
      dbSpan.setStatus({ code: SpanStatusCode.ERROR });
      dbSpan.recordException(error);
      dbSpan.end();
      throw error;
    }

    span.end();
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR });
    span.recordException(error);
    span.end();
    throw error;
  }
}
```
<!-- CODE_BLOCK_END id=c2 -->

💡

Wondering how OpenTelemetry stacks up against traditional APM tools? This post breaks down the key differences:

[OpenTelemetry vs Traditional APM Tools.](https://last9.io/blog/opentelemetry-vs-traditional-apm-tools/)

## Advanced Tracing Techniques

Once you've got basic tracing in place, these advanced techniques can take your observability to the next level.

### Distributed Context Management

In complex systems, you need to manage context beyond just trace IDs. The W3C Trace Context specification provides standards for:

- traceparent: Contains the trace ID and parent span ID
- tracestate: Allows vendors to add custom context data

Using these headers ensures your tracing works across different services and vendors.

### Correlation Between Traces, Metrics, and Logs

The real power of observability comes from connecting different signals:

- Exemplar traces: Link metrics to the traces that generated them
- Trace IDs in logs: Add trace IDs to log messages for cross-referencing
- Custom attributes: Use consistent attributes across all telemetry types

### Error Handling and Exception Tracking

When exceptions occur, spans can provide crucial context:

- Mark spans with error status
- Record exceptions with stack traces
- Add events to spans that show the error's progression
- Create baggage items that carry error context across service boundaries

💡

For a deeper look at staying ahead of issues and improving system reliability, check out this post on proactive monitoring:

[Proactive Monitoring.](https://last9.io/blog/proactive-monitoring/)

## Real-World Tracing Patterns and Anti-Patterns

### Effective Tracing Patterns

Meaningful span names: Use consistent naming conventions like service_name/operation
Right granularity: Create spans for significant operations, not every function call
Proper context propagation: Ensure trace context flows through all communication channels
Useful attributes: Add attributes that help with troubleshooting, like user IDs or feature flags
Performance awareness: Watch out for the overhead of excessive span creation

### Tracing Anti-Patterns to Avoid

Over-instrumentation: Creating too many spans can cause performance issues
Missing context: Failing to propagate context breaks traces across service boundaries
Inconsistent naming: Using different naming standards makes traces harder to interpret
Too much data: Putting large payloads in spans can overwhelm your tracing backend
Ignoring third-party services: Missing spans for external calls creates blind spots

💡

Explore how observability plays a crucial role in the performance and reliability of LLMs:

[LLM Observability.](https://last9.io/blog/llm-observability/)

## Business Value of Traces and Spans: Beyond Technical Benefits

Traces aren't just for troubleshooting—they can provide business insights too:

- Track critical user journeys from end-to-end
- Measure the performance of key business operations
- Set SLOs (Service Level Objectives) based on trace data
- Quantify the cost of performance issues in real user terms
- Create business context by adding relevant attributes to spans

When you can show how technical improvements affect user experience and business metrics, you bridge the gap between DevOps and business stakeholders.

## Conclusion

Traces and spans give you X-ray vision into your distributed systems. They reveal the hidden connections between services, pinpoint performance bottlenecks, and dramatically speed up debugging.

As systems grow more complex, this kind of observability isn't a luxury—it's essential.

💡

If you'd like to continue the conversation about distributed tracing and observability, join our

[Discord Community where DevOps professionals share their experiences and best practices!](https://discord.com/invite/W8gMppQC4b)

## FAQs

### What's the difference between tracing and logging?

Logging captures discrete events, while tracing shows the relationships between operations across services. Logs tell you what happened; traces show you how it happened.

### Will adding tracing slow down my application?

Modern tracing libraries add minimal overhead — typically less than 3% performance impact when properly configured. With sampling, you can further reduce this impact.

### Do I need to modify all my code to add tracing?

Not necessarily. Many frameworks offer automatic instrumentation that adds tracing with minimal code changes. OpenTelemetry provides auto-instrumentation for popular frameworks in most languages.

### How much data does distributed tracing generate?

It varies widely based on traffic, sampling rate, and span detail. Plan for anywhere from gigabytes to terabytes per day for busy systems. That's why choosing the right observability platform matters for cost control.

### Can traces help with security and compliance?

Yes! Traces create an audit trail of request flow through your system. With the right attributes, you can track which users or services accessed what data and when.

### How do traces and spans fit with other observability signals?

Traces complement metrics and logs. Metrics show system health at a high level, logs provide detailed events, and traces connect the dots to show request flows across services.

Topics

[Observability](/blog/tag/observability/)

[Monitoring](/blog/tag/monitoring/)

About the authors

![Anjali Udasi](https://last9.ghost.io/content/images/2024/08/profile_pic.jpeg)

[Anjali Udasi](/blog/authors/anjali/)

Helping to make the tech a little less intimidating. I

#### Contents

https://discord.com/invite/Q3p2EEucx9/

https://www.linkedin.com/company/last9/

https://youtube.com/@last9/

https://x.com/last9io/

![Last9 keyboard illustration](/_astro/buttons.SzdkIwcl_Z28vC7U.webp)

## Start observing for free. No lock-in.

[Book demo](/schedule-demo/)

[OPENTELEMETRY • PROMETHEUS](/docs/integrations/)

Just update your config. Start seeing data on Last9 in seconds.

[DATADOG • NEW RELIC • OTHERS](/docs/integrations/)

We've got you covered. Bring over your dashboards & alerts in one click.

[BUILT ON OPEN STANDARDS](/docs/integrations/)

100+ integrations. OTel native, works with your existing stack.

4.8/5

[G2 Reviews](https://www.g2.com/products/last9-last9/reviews)

![Gartner Cool Vendor 2025](/_astro/gartner-cool-vendor-badge.ClTJIiRB_sMwyD.webp)

Gartner Cool Vendor 2025

![High Performer](/_astro/high-performer-badge.BCroQ4N5_1fldwe.svg)

High Performer

![Best Usability](/_astro/best-usability-badge.mZNSvnQA_1fldwe.svg)

Best Usability

![Highest User Adoption](/_astro/highest-user-adoption-badge.DlXpV0dv_1fldwe.svg)

Highest User Adoption
