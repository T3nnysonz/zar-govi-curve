# Final Report

## Written overview/Summary

This project primarily provides a means through which bonds may be bootstrapped. Through it a local Webapp can be run on which bond databases may be referenced and bootstrapped with customisation included. The secondary feature is the testing suite, which provides developers a means through which to test the validity of the bootstrapper. The highlight of the testing suite is the provided ability to test the bootstrapper against sample Murex data.

## Completion Status

| Subtask | Achieved |
|---------|----------|
|A working curve engine (Python) that bootstraps a ZAR government (govi) zero curve from government bond inputs. | Yes |
|A basic webapp that lets a user load/enter bond data, run bootstrap, and visualize/export the resulting curve. | Yes |
|Outputs validated against a Murex environment: curve outputs are reconciled to Murex results using an agreed comparison method and tolerance, with differences explained and documented.| Somewhat, the curve was validated against Murex, but I failed to meet strict tolerance. |
|Clear documentation in Markdown, including concept notes (TVM, bond pricing, bootstrapping steps, conventions), “how to run”, “how it works”, and Mermaid diagrams where helpful.| Yes |
|A daily written report submitted by 17:00 each working day. | Yes |

## Lessons learned:

- Time value of money: I learned the basic concepts of the time value of money and how to quantify this fact using present values.
- Interpolation techniques: I was introduced to many interpolation techniques beyond the standard linear interpolation.
- Bonds: I learned what bonds are.
- Bootstrapping: I learned the underlying logic of bootstrapping at a fairly thorough level.
- GitHub: I learned how to upload code projects to GitHub and regularly update the online repository.
- Streamlit: I learned basic streamlit syntax, which will be helpful in my own mini-coding projects in the future.
- Mermaid: I learned how to create flow charts on mermaid which provide me a tool for communicating complex system processes.
- Discipline: I learned how to dedicate 8-9 hours a day to a project for many days in a row.
- Debugging: I became much more proficient in code debugging.
- Healthy work relationship with AI: I learned to neither neglect the opinions of AI when doing projects, (due to its superior understanding of the underlying finance) nor be too reliant on it as it was never able to debug my code.

## Next Steps:

- Improve bootstrapping quality to lower discrepency with Murex results.
- Improve csv importing system
- Improve swap bootstrapping algorithm
- Switch to Jacobian system