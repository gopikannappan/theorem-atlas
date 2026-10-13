# Organization transfer plan

The owner selected a new GitHub organization named **theorem-atlas** on 2026-10-13. A public-account lookup returned 404; GitHub must confirm actual availability during signup. No organization or repository transfer has been performed.

## Create the destination

The account owner must use [GitHub organization signup](https://github.com/organizations/plan), choose GitHub Free for this public project, and create `theorem-atlas`. The authenticated tools available here do not create personal-account organizations; signup includes owner-only account/billing/contact steps. Keep the owner account's two-factor authentication enabled. Add a second trusted organization owner when one is available for recovery; do not invite unknown accounts merely to satisfy a checklist.

Once created, confirm this account can administer the organization and create repositories there. The target must not already contain `theorem-atlas` or a conflicting fork. Then transfer the existing repository; do not replace it with a new copy, which would discard history, discussions, and issue/PR provenance.

## Preserve deployment and references

Keep the repository name **theorem-atlas** and the **/theorem-atlas/** site path. The new Pages hostname would be `theorem-atlas.github.io`; the resulting URL would be `https://theorem-atlas.github.io/theorem-atlas/`. The current site is `https://gopikannappan.github.io/theorem-atlas/`.

GitHub redirects repository URLs after transfer but does not automatically redirect the old Pages URL. Before transferring, decide how to retain the old Pages address: a separate redirect-only Pages repository under the original account is possible, but creating a repository at the previous Git repository location would remove GitHub's repository redirects. A later custom domain can provide a stable public site address, but no domain has been selected. Plan this explicitly rather than assuming the old website URL will continue to work.

After transfer:

1. Update the local Git remote, public project links, README site URL, issue contact link, and SECURITY private-report URL.
2. Recheck branch protection, required build context, Actions permissions/pins, private reporting, secret scanning, Dependabot, CodeQL, and Pages environment/deployment policy. Organization defaults can affect transferred repositories.
3. Update CODEOWNERS to existing maintainers or real organization teams. Set default organization permissions conservatively and give write/admin access only to people who need it.
4. Rebuild/deploy and verify the site, static data, record deep links, and source attribution page under the unchanged path.

No transfer should run merely because a public account with the desired name appears: verify that the project owner controls it and confirm the destination explicitly.

References: [GitHub organizations](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/about-organizations), [repository transfer behavior](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository).
