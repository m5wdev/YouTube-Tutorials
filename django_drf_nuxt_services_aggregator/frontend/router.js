import Router from 'vue-router'

export function createRouter(ssrContext, createDefaultRouter, routerOptions) {
  const options = routerOptions || createDefaultRouter(ssrContext).options

  let routesDirectory = null

  if (process.server && ssrContext && ssrContext.nuxt && ssrContext.req) {
    const req = ssrContext.req

    const domainLevel = (req.headers.host.match(/\./g) || []).length + 1

    // Get routes directory by hostname

    routesDirectory = domainLevel > 1 ? 'sub-domain' : 'root-domain'
    // Save to the object that will be sent to the client as inline-script
    ssrContext.nuxt.routesDirectory = routesDirectory
  }
  if (process.client) {
    // Get what we saved on SSR
    if (window.__NUXT__ && window.__NUXT__.routesDirectory) {
      routesDirectory = window.__NUXT__.routesDirectory
    }
  }

  function isUnderDirectory(route, directory) {
    const path = route.path
    return path === '/' + directory || path.startsWith('/' + directory + '/')
  }

  let newRoutes = options.routes

  if (routesDirectory) {
    newRoutes = options.routes
      .filter((route) => {
        // remove routes from other directories
        const toRemove =
          routesDirectory === 'sub-domain'
            ? 'root-domain'
            : 'sub-domain'
        return !isUnderDirectory(route, toRemove)
      })
      .map((route) => {
        // remove directory from path and name
        if (isUnderDirectory(route, routesDirectory)) {
          return {
            ...route,
            path: route.path.substr(routesDirectory.length + 1) || '/',
            name: route.name || 'index'
          }
        }
        return route
      })
  }

  return new Router({
    ...options,
    routes: newRoutes
  })
}
