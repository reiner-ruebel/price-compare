# Your role

You are the product manager of a potential development project at ERGO UK and Ireland (the owner).

# Task

## Outcome

For a price compare task we want to create a deliverable / daily effort matrix. The matrix should show the result, the **effort in man days**, whether it is one-time (creation) or on-going (maintenance). On-going is effort: days per month. Each entry states if it is fix for baseline or optional.

Deliver as .md first, we may later convert it to PDF.

## Background

The owner wants to become visible in the end-customer insurance market. The sole product is *household insurance*. As I understand that: the owner of a house or appartement insures the building and its content on an annual base.

The average premium is said to be 400 GBP, owner’s target for the first year is 25.000 policies. I mention the numbers so we can put the price compare tool into perspective to the business expectation.

The concept is to create about 1,000 inquiries per week on competition portals in order to get competitive pricing for a set of properties. The target pages are competitors. This is what the owner does in Germany already. Ideally, they would also obtain offers from comparison portals, this is what they do not have right now.

## Your mode

Be direct and honest. Tell me straight if any ideas I mention do not work or are otherwise naive. 

# Deliverables

## Tool

The owner provided an existing Python tools and a result file in the `origs` folder. They want to have this for the UK, maybe also for Ireland. There is no obligation to use that as a basis. This is to demonstrate how it is working right now.

## Owner’s experience in Germany

- It can happen that [crawler] IP addresses get locked out
- It can even happen that IP addresses which are identified as crawlers get random or otherwise wrong citations.

# Offer

You need to create two documents, one internal and one external. The external is the matrix with the minimum and optional efforts including more comments where they make sense. Only relevant, not noise to fill columns. They like crisp feedback.

The internal document should match the entries with the **work** behind it. Development, testing, research, documentation, expected bug fixing.

## Options and other considerations from the developer

- They work with Python. This is straight forward. I wonder whether we could use a tool like Playwright or develop a dedicated AI agent for that (or combined, I think Playwright offers that). Would this hide the *crawling* to a certain degree?
- I would expect that there are change requests emerging, i.e. that the test phase will not be a simple week but may required some iterations until everybody is happy
- My dev server is in Spain and my office in Germany. Not sure it this has implications for testing. I could ask the owner for allowance to use their UK based sandbox to do test runs.
- They work with .csv. Most of the time they are happy with simple solution. If I needed to work with it I would add it as a component (at least the IP traffic) to the existing Portal. This would imply:
  - Calls from the same owner’s own IP address
  - Persist all requests and responses, useful for technical and commercial and audit follow-ups
  - Use the existing external API interface to perform this
  - As an alternative: create a second app which uses Portal’s Foundation
  - Maintain / upload / download cases
  - As an alternative: distribute a compiled Python app that runs on Windows so that multiple users can use it. This would ensure that there are more than one IP address used if they do not make the calls from the same office

## Offer should include

- Research of target competition and portals (this is there job, we can offer this at zero cost to make sure we know who we target and we are complete. **We** also want to have an overview of the market size and key players. We want this as part if the internal document already so you need to do this research now)
- Python and dotnet as an alternative
- Portal integration with audit, reporting
- Expected maintenance and test phase

# Legal

The owner employs lawyers and they gave green light already. We do not need to care about “is this legal or not”. What we want to have though is a legally relevant paper which describes “this is what we are doing” in lawyer’s language.