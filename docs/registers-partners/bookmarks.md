# Personal and shared bookmark register

Each row has its own `bookmark.rowid`. Two bookmarks with the same title or destination remain two rows. The register returns the saved date `dateb`, owner `fk_user`, title, URL, window target, favicon and display position. A left join from `fk_user` to `user.rowid` supplies the owner's login and names. A shared entry with an empty owner survives this join.

| Input or condition | Effect |
| --- | --- |
| Bookmark entity | Include entries in the visible bookmark entities. Administrator status retains this scope. |
| Owner | An ordinary user sees their own entries and the shared entries with an owner of zero or null. An administrator can also see entries owned by another user within scope. |
| `search_title` | A nonempty value uses the common text matcher against the title. The destination, user login and target are outside this search. |
| Sort and page | The default is ascending position. A chosen field is followed by position as a secondary sort. With equal positions no unique-ID tie break is specified. The page index is zero-based. Searching, clearing or selecting a negative page resets it to zero. |
| Count | If full counts are enabled, count visible joined rows after filtering. A page offset strictly greater than the count resets to zero. The page query asks for one additional row to establish whether more entries follow. |

The register requires bookmark access. General deletion needs `bookmark.supprimer`. On an individual entry its owner can also remove it with `bookmark.creer`. For a user without the delete-all grant, bulk processing intersects the submitted IDs with entries owned by that user in their visible entities. A shared entry is viewable but falls outside that ownership set. Search and clear actions cancel pending bulk selection actions. Deleting a bookmark removes its navigation record, with no change to the bookmarked business document.

For a fixture in one visible entity, give user 8 two entries titled “Dispatch” at positions 2 and 4, give user 9 one “Dispatch” at position 1, and add a shared “Dispatch guide” at position 3. Add a shared “Dispatch” in another, unshared entity. Searching for `Dispatch` returns positions 2, 3 and 4 to user 8. The administrator sees positions 1 through 4. The same ordinary user can have two owned entries eligible for deletion even though the search returned three entries.
