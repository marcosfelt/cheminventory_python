workflow "New workflow" {
  resolves = ["Publish Python Package"]
  on = "release"
}

action "Publish Python Package" {
  uses = "mariamrf/py-package-publish-action@v0.0.2"
}
